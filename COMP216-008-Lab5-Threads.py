import os
import requests
import threading
import time
import argparse

def download_file(url, pathname, download_folder=None):
    if download_folder is None:
        download_folder = os.getcwd()

    # Create the download folder if it doesn't exist
    os.makedirs(download_folder, exist_ok=True)

    # Construct the full path for saving
    full_path = os.path.join(download_folder, pathname)

    # Download the file
    try:
        with requests.get(url) as response:
            response.raise_for_status()
            with open(full_path, 'wb') as file:
                file.write(response.content)
    except requests.exceptions.HTTPError as e:
        print(f"Failed to download file from URL: {url}")
        print(f"Error message: {str(e)}")

    print(f"Downloaded file: {full_path}")
    return full_path


def download_images_sequentially(urls, download_folder=None):
    downloaded_files = []
    for i, url in enumerate(urls):
        filename = f'image{i + 1}.jpg'
        full_path = download_file(url, filename, download_folder)
        downloaded_files.append(full_path)
    return downloaded_files


def download_images_with_threads(urls, download_folder=None):
    downloaded_files = []

    def download_image(url, filename, download_folder):
        full_path = download_file(url, filename, download_folder)
        downloaded_files.append(full_path)

    threads = []
    start_time = time.time()

    for i, url in enumerate(urls):
        filename = f'image{i + 1}.jpg'
        thread = threading.Thread(target=download_image, args=(url, filename, download_folder))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Time taken for threaded download: {end_time - start_time} seconds")

    return downloaded_files


def main(urls):
    parser = argparse.ArgumentParser(description="Download images either sequentially or with threads.")
    parser.add_argument("method", choices=["serial", "threaded"], help="Choose 'serial' or 'threaded' for download method.")
    parser.add_argument("-d", "--data-folder", help="Specify the data folder to download images to.")

    args = parser.parse_args()

    download_method = None

    if args.method == "serial":
        download_method = download_images_sequentially
    elif args.method == "threaded":
        download_method = download_images_with_threads
    else:
        parser.error("Invalid method. Please choose either 'serial' or 'threaded'.")

    download_folder = args.data_folder or os.getcwd()

    try:
        download_method(urls, download_folder)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    urls = [
        'https://th.bing.com/th/id/OIP.z-dkECmUFma29zYrb27JkwAAAA?w=264&h=180&c=7&r=0&o=5&pid=1.7',
        'https://th.bing.com/th/id/OIP.MhwSzfXnBG1MpuuA6IFi-AAAAA?w=218&h=180&c=7&r=0&o=5&pid=1.7',
        'https://th.bing.com/th/id/OIP.m8b7Y9-81Q4UMCBMaFkw2QAAAA?w=198&h=180&c=7&r=0&o=5&pid=1.7',
        'https://th.bing.com/th/id/OIP.XN9D7tH47WNJ8h214YgqTwAAAA?w=220&h=180&c=7&r=0&o=5&pid=1.7',
        'https://th.bing.com/th/id/OIP.cFvfW8dARmuVtR3zOxfTSAHaE9?w=274&h=183&c=7&r=0&o=5&pid=1.7',
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQJPVGXDHdZhb2QgMPu39gg8CaQTJzj_yJtx-sjJRg3XEpOk8Dc8a3i6RmROg&s',
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTlkN-p_QUIV3aytp0a4s-hmfwF-1SUF3uEj6w8FUyF0FZLtX-IyHe-O7BVpA&s',
        'https://th.bing.com/th/id/OIP.JYXSCIpGskpiOxYTw1vuwgAAAA?w=252&h=180&c=7&r=0&o=5&pid=1.7',
        'https://th.bing.com/th/id/OIP.QjWOHkojgYSz1LhaypSB-gAAAA?w=190&h=180&c=7&r=0&o=5&pid=1.7',
        'https://th.bing.com/th/id/OIP.Wlfm_lF4VWlYLiPNfbmbDwHaHa?w=181&h=181&c=7&r=0&o=5&pid=1.7',
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRCyeYzqq7HVoBoivyFFx53TSockvC280EbUIVZOn_A9qzMh_yZT-vfi2CVlg&s',
        'https://th.bing.com/th/id/OIP.C6q29lesR7-Ork5YKuI6LwAAAA?w=257&h=180&c=7&r=0&o=5&pid=1.7',
        'https://th.bing.com/th/id/OIP.A7o1Bm-XNr9A_4pLPCCujgAAAA?w=252&h=180&c=7&r=0&o=5&pid=1.7',
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ_Yjn7kNEUDHaue2Df0jRm-qRAfMC2bIVDqC5Nkoye1ZqcjkXZ64e5O1HkrA&s',
        'https://th.bing.com/th/id/OIP.AroTG9KnmisPIhICyGjoDAHaFj?w=223&h=180&c=7&r=0&o=5&pid=1.7',
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRCyeYzqq7HVoBoivyFFx53TSockvC280EbUIVZOn_A9qzMh_yZT-vfi2CVlg&s',
        'https://th.bing.com/th/id/OIP.pGTxkbwreLj7l2ORZrtA8gAAAA?w=147&h=184&c=7&r=0&o=5&pid=1.7',
        'https://th.bing.com/th/id/OIP.5SaLUh616MU7KDIP2_0VCwAAAA?w=204&h=180&c=7&r=0&o=5&pid=1.7',
        'https://th.bing.com/th/id/OIP.S-lrZd2TFhSEpI3VRQyKqQAAAA?w=173&h=180&c=7&r=0&o=5&pid=1.7',
        'https://th.bing.com/th/id/OIP.sDmZWxXBrF329vZvDu2HrAAAAA?w=266&h=180&c=7&r=0&o=5&pid=1.7',
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQJPVGXDHdZhb2QgMPu39gg8CaQTJzj_yJtx-sjJRg3XEpOk8Dc8a3i6RmROg&s',
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTLbcrbIKRXnTEx7OhgHIJhSS7a-tmcphA9H-yKJoCG9R7agj2tRdQv4okBtw&s',
        'https://th.bing.com/th/id/OIP.OeLv1q1dEfGkl1bRHfM5awHaFj?w=240&h=180&c=7&r=0&o=5&pid=1.7',
        'https://th.bing.com/th/id/OIP.MksSZEmu5Cgly2HNvRp4NQAAAA?w=180&h=163&c=7&r=0&o=5&pid=1.7',
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRky_bBsYjQ2EMkldpbtq_SQFckuUjsK9bwaqy_y7EGtjUoSKDeT_vhTnsSJA&s'
    ]

    # url = urls[0]
    # pathname = 'image1.jpg'
    # download_file(url, pathname)
    #
    # download_images_sequentially(urls)
    # download_images_with_threads(urls)

    main(urls)

