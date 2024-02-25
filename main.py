from flet import Page, app, Text

from drag_and_drop_list import DragAndDropListView


def main(page: Page):
    page.window_width = 200

    ft_list = DragAndDropListView(
        controls=[
            Text(f"Line {i}") for i in range(100)
        ],
        auto_scroll=True,
    )

    page.add(ft_list)
    page.scroll = 'always'

    page.update()


if __name__ == '__main__':
    app(main)
