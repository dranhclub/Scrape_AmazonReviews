# Scrape_AmazonReviews

# Cách chạy
- Cần cài `scrapy` để chạy:  
`pip install scrapy`
- Sau đó chạy lệnh:  
`scrapy runspider ./spiders/AmazonReviews.py -o output.json` 
- hoặc  
`./run-spider.sh`

# Cách xử lý khi bị chặn
- Dùng trình duyệt, truy cập vào trang review của sản phẩm bất kỳ, ví dụ:  
https://www.amazon.com/product-reviews/B00MGK9Z8U/?ie=UTF8&reviewerType=all_reviews&pageNumber=1&sortBy=recent

- Mở devTool (F12), chọn thẻ Network, chuột phải vào item đầu tiên (chính là toàn bộ webpage), chọn copy cURL

- Vào https://curl.trillworks.com/ , paste nội dung cURL vào ô bên trái

- Lấy object header ở ô bên phải, dán vào object header tương ứng trong AmazonReviews.py

        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                headers = {
                    ....
                })