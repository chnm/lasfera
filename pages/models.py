from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.fields import RichTextField
from wagtail.models import Page


class AboutPage(RoutablePageMixin, Page):
    body = RichTextField(blank=True)
    team = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body", classname="full"),
        FieldPanel("team", classname="full"),
    ]


class SitePage(Page):
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel("body", classname="full"),
    ]
    template = "pages/site_page.html"
