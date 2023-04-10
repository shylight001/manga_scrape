from PIL import Image  # install by > python3 -m pip install --upgrade Pillow  # ref. https://pillow.readthedocs.io/en/latest/installation.html#basic-installation
import os
import re
import pandas as pd 

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]
    
manga_title = input("Manga name to combine:\n") #"冲突"    
manga_path = f'Downloads\\{manga_title}\\'

if not os.path.exists(f"{manga_path}pdf\\"):
        os.makedirs(f"{manga_path}pdf\\")
        
chapters = os.listdir(manga_path)
chapters.remove('pdf')  
chapters.sort(key=natural_keys)
    
failed_chapter = []
for chapter in chapters:
    try:
        pdf_path = f"{manga_path}pdf\\{chapter}.pdf"
        if os.path.isfile(pdf_path):
            print(f"pdf {pdf_path} is created")
            continue
        chapter_path = manga_path+chapter+"\\"
        images_files = os.listdir(chapter_path)
        images_files.sort(key=natural_keys)
        
        images = []
        for f in images_files:
            image = Image.open(chapter_path + f)
            if image.mode == 'RGBA':
                print(chapter_path + f)
                image = image.convert('RGB')
            images.append(image)
        print(f"saving pdf {pdf_path}...")
        images[0].save(
            pdf_path, "PDF" ,quality=100, save_all=True, append_images=images[1:]
        )
    except Exception as e:
        print(f"XXXX failed chapter {chapter} {e}")
        failed_chapter.append([chapter,e])
        
if failed_chapter: 
    df = pd.DataFrame(failed_chapter) 
    df.to_csv(f"failed_combine_chapter_{manga_title}.csv", index=False)    
    
print(f"finished creation of {manga_title}")