# Alhamdulillah

from icrawler.builtin import BingImageCrawler, GoogleImageCrawler




num_of_images = 150
download_path = '../data/images/'

shikhs = [
    ['الشخ محمود خليل الحصري', 'hossary'],
    ['الشيخ محمود علي البنا', 'banaa'],
    ['الشيخ عبدالباسط عبدالصمد', 'abdelbaset'],
    ['الشيخ مشاري راشد العفاسي', 'meshary'],
    ['الشيخ علاء حامد', 'alaa']
]


for shikh in shikhs:
    folder_name = shikh[1]

    # Create crawler and download  images
    print(f"Downloading up to {num_of_images * 2} training images for '{shikh[0]}'...")

    # Download from Bing
    crawler = BingImageCrawler(storage = {'root_dir': download_path + folder_name})
    crawler.crawl(keyword = shikh[0], max_num = num_of_images)

    # Downloade from Google
    google_crawler = GoogleImageCrawler(storage = {'root_dir' : download_path + folder_name})
    google_crawler.crawl(keyword = shikh[0], max_num = num_of_images)


    print(f"Done with '{shikh[0]}'\n" + "-" * 100)

print('Finished -- Alhamdulillah')
print(100 * '-')




