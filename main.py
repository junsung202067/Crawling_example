
from playwright.sync_api import sync_playwright
import time


def save_kw_notice_html():
    with sync_playwright() as p:
        # 크롬 브라우저 사용
        # 브라우저를 보여주겠다 (headless = false)
        browser = p.chromium.launch(headless = False)
        page = browser.new_page()

        url = "https://www.kw.ac.kr/ko/life/notice.jsp?srCategoryId=&mode=list&searchKey=1&searchVal="
        page.goto(url,wait_until="networkidle")


        for _ in range(5):
            page.keyboard.press(key="PageDown")
            time.sleep(0.2)

        html_content = page.content()
        with open(file="kw_notice.html",mode="w",encoding="utf-8") as f:
            f.write(html_content)

        print("페이지 콘텐츠를 kw_notice.html로 저장했습니다.")

def scrape_kw_notice():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = False, slow_mo = 50)
        page = browser.new_page()
        url = "https://www.kw.ac.kr/ko/life/notice.jsp?srCategoryId=&mode=list&searchKey=1&searchVal="
        print("광운대 공지사항 페이지로 이동합니다")

        try:
            page.goto(url,wait_until="networkidle", timeout=10000)
        except TimeoutError:
            print("페이지 로딩 시간이 초과되었습니다")

        for _ in range(5):
            page.keyboard.press(key ="PageDown")
            time.sleep(0.2)

        items = page.locator("div.list-box  > div > ul > li").all()
        print(  f"총 {len(items)}개의 공지사항을 찾았습니다.")


        all_notices = []
        for i,item_locator in enumerate(iterable=items[:]):
            link = None
            title = None
            category = None
            data = None
            new_icon_text = ""
            file_icon_text = ""

            try:
                # li에 속한 a 태그 추출
                a_locator = item_locator.locator("div.board-text > a")

                # 링크 정보 추출
                link = a_locator.get_attribute(name="href")
                full_link = f"https://www.kw.ac.kr{link}"
                

                # 카테고리 정보 추출
                category = a_locator.locator("strong.category")
                if category.count() > 0:
                    category = category.inner_text().strip()
                else:
                    category = "카테고리 없음"

                # new 아이콘 텍스트 추출
                new_icon_locator = a_locator.locator("span.ico-new")
                if new_icon_locator.count() > 0:
                    new_icon_text = new_icon_locator.inner_text().strip()
                else:
                    new_icon_text = ""

                # 파일 아이콘 텍스트 추출
                file_icon_locator = a_locator.locator("span.ico-file")
                if file_icon_locator.count() > 0:
                    file_icon_text = file_icon_locator.inner_text().strip()
                else:
                    file_icon_text = ""

                # 공지사항을 추출하기 위해 a href 전체 추출
                full_title = a_locator.inner_text()

                # 전체 제목에서 카테고리와 new 아이콘 텍스트 제거
                title = full_title.replace(category, "").replace(new_icon_text, "").replace(file_icon_text, "").strip()

                print(f"[{i}] 링크: {full_link}")
                print(f"[{i}] 카테고리: {category}")
                print(f"[{i}] 제목: {title}")
                print("--------------------------------------------------") 

                

            except Exception as e:
                print(f"[{i}] 링크 또는 카테고리 정보를 가져오는 중 오류 발생: {e}")
            
            all_notices.append({
                "링크": full_link,
                "카테고리": category,
                "제목": title
            })

        return all_notices
    



if __name__ == "__main__":
    all = scrape_kw_notice()
    print(all)