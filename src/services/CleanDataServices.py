
from src.repositories.CleanDataRepository import CleanDataRepository
from src.services.PredictDataServices import PredictDataService
from src.utils.convert import queryResultToDict
from src.services.Service import Service
from src.utils.Scrapping.Scrapping import scrape_to_dataframe
from src.utils.Preprocessing.ImageProcessor import caption_images_in_folder
from src.utils.errorHandler import errorHandler
from src.utils.Preprocessing.TextProcessor import process_text
import os # Pastikan os diimpor
import json
cleanDataRepository = CleanDataRepository()
predictDataService = PredictDataService()

class CleanDataService(Service):
    @staticmethod
    def failedOrSuccessRequest(status, code, data):
        return {
            'status': status,
            "code": code,
            'data': data,
        }

    def getAllCleanData(self):
        try:
            data = cleanDataRepository.getAllCleanData()
            return cleanDataRepository.failedOrSuccessRequest('success', 200, queryResultToDict(data))
        except Exception as e:
            return cleanDataRepository.failedOrSuccessRequest('failed', 500, str(e))

    def createCleanData(self, data):
        """
        Menerima data dari Controller (misal: url, parent_id, child_id),
        melakukan scraping, preprocessing, lalu menyimpan ke database.
        
        Args:
            data (dict): Dictionary berisi 'url', 'parent_id', 'child_id'.
        """
        try:
            url = data['url']
            parent_id = data['parent_id']
            child_id = data['child_id']

            # 1. Cek apakah URL sudah ada di database
            existing = cleanDataRepository.getCleanDataByUrl(url)
            if existing:
                existing_data = queryResultToDict([existing])[0]
                print(f"URL sudah ada: {url}. Melewatkan scraping, langsung ke prediksi.")
                data_for_prediction = {
                    'text': existing_data['text'],
                    'url': existing_data['url'],
                    'parent_id': existing_data['parent_id'],
                    'child_id': existing_data['child_id']
                }
                prediction_result = predictDataService.createPredictData(data_for_prediction)
                if prediction_result['status'] == 'failed':
                    return self.failedOrSuccessRequest('failed', prediction_result['code'], prediction_result['data'])
                return self.failedOrSuccessRequest('success', prediction_result['code'], prediction_result['data'])
            # 2. Lakukan Scraping
            print(f"Memulai scraping untuk URL: {url}")
            df_scraped = scrape_to_dataframe(url, save_images=True)
            if df_scraped.empty:
                return self.failedOrSuccessRequest('failed', 404, "Gagal mendapatkan konten dari URL.")
            
            # Ambil data dari baris pertama DataFrame hasil scraping
            scraped_result = df_scraped.iloc[0]
            raw_text = scraped_result['text']
            image_links_str = scraped_result['image_urls']
            image_folder = scraped_result['image_folder']
            
            # 3. Lakukan Image Captioning
            combined_text = raw_text
            if image_folder:
                print(f"Memulai image captioning untuk gambar di folder: {image_folder}")
                captions_text = ""
                # Pastikan folder gambar benar-benar ada dan tidak kosong
                if image_folder and os.path.isdir(image_folder):
                    print(f"Memulai image captioning untuk gambar di folder: {image_folder}")
                    df_captions = caption_images_in_folder(image_folder, delete_corrupted=False)
                    
                    if not df_captions.empty:
                        # Ambil semua caption dan gabungkan menjadi satu string
                        captions_list = df_captions['Caption'].tolist()
                        captions_text = '. '.join(captions_list)
                        print(f"Caption yang dihasilkan: {captions_text[:150]}...")
                    else:
                        print("Tidak ada caption yang berhasil dibuat.")
                else:
                    print("Tidak ada folder gambar untuk diproses captioning.")

                # 4. Gabungkan Teks Scraped dengan Teks Caption
                # Tambahkan spasi dan titik untuk pemisah yang jelas
                combined_text = f"{raw_text}. {captions_text}".strip()

            # 3. Lakukan Preprocessing Teks
            print("Memulai preprocessing teks...")
            clean_text, final_tokens = process_text(combined_text)
            if not clean_text:
                return self.failedOrSuccessRequest('failed', 500, "Teks kosong setelah preprocessing.")
            print("Preprocessing teks selesai.")

            # 4. Siapkan data untuk disimpan
            data_to_save = {
                "child_id": child_id,
                "parent_id": parent_id,
                "url": url,
                "text": clean_text, 
                "raw_text": combined_text,
                "stopword_removed_tokens": final_tokens,
                "link_gambar": image_links_str,
                "folder_gambar": image_folder
            }
            print(f"Data yang akan disimpan: {data_to_save}")
            # 5. Panggil Repository untuk menyimpan
            new_record = cleanDataRepository.createNewCleanData(data_to_save)
            record_dict = queryResultToDict([new_record])
            prediction_result= predictDataService.createPredictData(record_dict[0])
            if prediction_result['status'] == 'failed':
                return self.failedOrSuccessRequest('failed', prediction_result['code'], prediction_result['data'])
            return self.failedOrSuccessRequest('success', prediction_result['code'], prediction_result['data'])
        except ValueError as e:
            return self.failedOrSuccessRequest('failed', 400, str(e)) # Bad request (misal: data tidak lengkap)
        except Exception as e:
            # Tangani error umum lainnya
            print(f"ERROR di CleanDataService: {e}")
            return self.failedOrSuccessRequest('failed', 500, f"Terjadi kesalahan internal: {e}")
