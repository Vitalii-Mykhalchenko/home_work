import sys
import os
from pathlib import Path
import shutil

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
FOLDER_NAME = {
    ('JPEG', 'PNG', 'JPG', 'SVG'): "images",
    ('AVI', 'MP4', 'MOV', 'MKV'): "video",
    ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'): "documents",
    ('MP3', 'OGG', 'WAV', 'AMR'): "audio",
    ('ZIP', 'GZ', 'TAR'): "archives"
}


def translate(name:str): # транслитерирує ім'я + замінює спец символи
    TRANS = {}
    string = ""
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION): 
        TRANS[ord(c)] = l    
        TRANS[ord(c.upper())] = l.upper()
    for el in name:
        if el.isalnum() or el.isspace():
            unicode = ord(el)
            string += TRANS.get(unicode, el)
        else:
            string += "_"
    return(string)


def get_folder_name_extensions(extensions): # отримуємо ім'я папки згідно з розширенням або отримуємо None  якщо розширення не відоме
    for el in FOLDER_NAME:
        if extensions.lower() in map(str.lower,el):
            return FOLDER_NAME.get(el)


def delete_empty_folder (path:Path): # видаляємо папки якщо вона пуста
    try:
        if path.is_dir() and len(list(path.iterdir()))==0:
            path.rmdir()
            print(f"папка видалена {path}")
    except:
        print( f"папка не пуста  {path}")


def proceed_file (path_file:Path, create_folders:list[Path]): # функція по обробки файлу
    file_extension = path_file.suffix[1:] # png, txt....
    file_name = path_file.stem            # назва файлу
    normalize_name =translate(file_name)  # видаляємо символи
    target_folder_name = get_folder_name_extensions(file_extension) #ім'я шляху (str)
    target_folder_path = next((path for path in create_folders if path.stem == target_folder_name), None) # знаходження шляху 
    if target_folder_path:
        if target_folder_path.stem == "archives":
            target_folder_path_normalize_name = target_folder_path.joinpath(normalize_name)
            shutil.unpack_archive(path_file,target_folder_path_normalize_name)
            path_file.unlink()
        else:
            normalize_name_file_extension = f"{normalize_name}.{file_extension}"
            target_folder_path_normalize_name_file_extension = target_folder_path.joinpath(normalize_name_file_extension) 
            shutil.move(path_file,target_folder_path_normalize_name_file_extension)
        return path_file.parent


def proceed_folder (path, create_folders): #функція яка обробляє файли
    if path in create_folders:
        return
    
    for el in path.iterdir():              # переебираємо вкладенні єлементи у папку
        if el.is_dir():                    # якщо це папка ми знову пеербираємо папку
            proceed_folder(el, create_folders) # рекурсивно визиваємо саму себе
        else:
            result_path=proceed_file(el,create_folders) # якщо це файл то обробляємо його як файл, результат виконання функції у батьківский каталог
            delete_empty_folder(result_path) #видаляємо батьківский каталог якщо він порожній         
    else:
        delete_empty_folder(path) # видаляємо порожні каталоги у корневій папці
        

def main (rood_folder:Path):
    create_folders = list(rood_folder.joinpath(folder)  for folder in FOLDER_NAME.values()) #створює список цільових папок 
    for el in create_folders:
        el.mkdir(exist_ok = True) # створюємо папки згідно каталогу


    proceed_folder(rood_folder,create_folders) # обробляємо корневий каталог


if __name__ == "__main__":
    if len(sys.argv) !=2:
        print("не корректна кількість аргументів")
    else:
        folder_name = Path(sys.argv[1])
        if not folder_name.is_dir():
            print("папка не існує")
        else:
            main(folder_name)


