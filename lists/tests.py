from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest, response
from django.template.loader import render_to_string

from lists.views import home_page  
from lists.models import Item

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')  
        self.assertEqual(found.func, home_page)
        
    # direct testing of content of response page, TESTING CONSTANTS
    '''    
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()  
        response = home_page(request)  
        html = response.content.decode('utf8')  
        self.assertTrue(html.startswith('<html>'))  
        self.assertIn('<title>To-Do lists</title>', html)  
        self.assertTrue(html.strip().endswith('</html>')) 
    '''
     
    # compare to equivalent file
    # weakness: need to decode ourself, craft our own httprequest
    '''
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')
        expected_html = render_to_string('home.html')
        self.assertEqual(html, expected_html)
    '''
        
    def test_uses_home_template(self):
        response = self.client.get('/')
        # from djangotestsuite
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)  
        new_item = Item.objects.first()  
        self.assertEqual(new_item.text, 'A new list item')  

    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        # checks for redirect to '/', redirect code is 302
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')
        
    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)
        
    def test_displays_all_list_items(self):
        Item.objects.create(text='Itemey 1')
        Item.objects.create(text='Itemey 2')
        
        response = self.client.get('/')
        
        self.assertIn('Itemey 1', response.content.decode())
        self.assertIn('Itemey 2', response.content.decode())
        
class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        # returns records as a list-like queryset
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')
        
    