from constant import *
from Tools.akuma_moe_download import fetchImageURLsInAkumaCollection 

def main():
    print(f"""
    ************************************************************************    
        Start scratching {TITLE} 
            Testing = {IS_TEST} 
            Update = {IS_UPDATE}
    ************************************************************************
    """)

    fetchImageURLsInAkumaCollection()

    print(f"""
    ************************************************************************   
        End scratching {TITLE} 
            Testing = {IS_TEST} 
            Update = {IS_UPDATE}
    ************************************************************************
    """)
    
if __name__ == "__main__":
    main()