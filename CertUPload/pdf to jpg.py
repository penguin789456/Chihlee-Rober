from pdf2image import convert_from_path
import os

UserName = "張佩胎"

def pdf_to_jpg(pdf_folder, output_folder):
    # 確保輸出資料夾存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍歷 PDF 資料夾中的所有 PDF 檔案
    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.lower().endswith(".pdf"):  # 檢查是否為 PDF
            pdf_path = os.path.join(pdf_folder, pdf_file)
            pdf_name = os.path.splitext(pdf_file)[0]  # 去掉副檔名作為輸出資料夾名稱
            pdf_output_folder = os.path.join(output_folder)

            try:
                # 轉換 PDF 為圖片
                images = convert_from_path(pdf_path)
                for i, image in enumerate(images):
                    # 將每一頁存成 JPG
                    output_file = os.path.join(pdf_output_folder, f"{pdf_name}.jpg")
                    image.save(output_file, 'JPEG')
                    print(f"已儲存: {output_file}")
            except Exception as e:
                print(f"轉換 {pdf_file} 時發生錯誤: {e}")

# 使用範例
pdf_folder = "C:\\Users\\binho\\Downloads\\Chihlee-Rober\\證照檔\\"+UserName  # 替換為存放 PDF 的資料夾路徑
output_folder = pdf_folder  # 輸出 JPG 的總資料夾
pdf_to_jpg(pdf_folder, output_folder)
