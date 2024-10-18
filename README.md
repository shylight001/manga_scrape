## This is a Selenium Scraper to scrape Manga Website that I am interested in.

Instruction on how to run the scraper:

+ Activate virtual environment:
   ```bash
   Scripts/activate.bat 
   ```
   or Powershell
   ```Powershell
   Scripts/activate.ps1
   ```
   deactivate virtual environment:
   ```bash
   Scripts/deactivate.bat 
   ```
+ Rename `constant.example.py` to `constant.py` and change variable values within.
+ Run `main.py` in virtual environment to scrape manga image, scraper will scrape urls in the file in `Resources` folder, specified in `constant.py`
+ Run `combine_image_to_pdf.py` to combine mange images to pdf if needed
