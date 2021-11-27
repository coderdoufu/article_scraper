import subprocess
import streamlit as st
import os
import sys
from retry import retry
import json

# scrapy
from scrapydemo.run_scraper import Scraper

@retry(exceptions=ValueError, tries=5, delay=6)
def open_json(output_file):
    with open(output_file,'r') as f:
        result = json.load(f)
    return result

#TODO
st.title('Crawling App')
st.write('This Streamlit application is a demo of how to use Scrapy to crawl a different number of websites. \
          Crawling is a very powerful yet underestimated tool in the industry. If you want to know more about Scrapy \
          and the use cases, please feel free to check out my latest post here: ')
st.markdown('⚠️ *Please note that you must abide by the website\'s terms of use before you do any crawling. \
             All the contents here are for educational purpose.*')

st.markdown("***")
crawl_type = st.selectbox(
    'Which content type you would like to crawl?',
    ['News', 'E-commerce (Coming soon)'])

st.markdown("***")
option_site = st.selectbox(
    'Which site you want to crawl?',
    ['Reuters', 'Channel News Asia'])

st.markdown("***")
data_dir = 'scrapydemo/scrapydemo/data'

def display_checkboxes(option_col):
    option_col.write("Display Options")
    display_options = {}
    display_options['image'] = option_col.checkbox("Image")
    display_options['url'] = option_col.checkbox("URL")
    display_options['title'] = option_col.checkbox("Title")
    display_options['author'] = option_col.checkbox("Author")
    display_options['published_time'] = option_col.checkbox("Published Time")
    display_options['updated_time'] = option_col.checkbox("Updated Time")
    display_options['body'] = option_col.checkbox("Content")

    return display_options

if option_site == 'Reuters':
    output_file = os.path.join(data_dir,'reuters.json')
    if os.path.isfile(output_file):
        os.remove(output_file)

    # read section categories file
    with open(os.path.join(data_dir, 'reuters_categories.json'),'rb') as f:
        section_categories_raw = json.load(f)
        section_categories = {}
        for section_cat in section_categories_raw:
            section_categories[section_cat['section_name']] = dict(zip(section_cat['section_cats'], section_cat['section_cats_url']))

    # read section file
    with open(os.path.join(data_dir,'reuters_sections.txt'),'r') as f:
        sections = f.readlines()[0].split(',')

    # user selection split into two columns
    option_left, option_right = st.columns(2)

    # selector box for section
    option_section = option_left.selectbox(
        'Which section you would like to crawl?',
        [section.capitalize() for section in sections]).lower()

    # selector box for number crawled articles
    option_number_article = option_left.selectbox(
        'How many articles you would like to crawl?',
        [1,2,3])

    # selector box for section categories
    option_section_category = ""
    if len(section_categories[option_section].keys()) != 0:
        option_section_category = option_left.selectbox(
            'Which category you would like to crawl?',
            section_categories[option_section].keys())

    display_options = display_checkboxes(option_right)

    option_section_category_url = section_categories[option_section].get(option_section_category,f'/{option_section}')
    st.write('ℹ️ Crawling url: www.reuters.com'+option_section_category_url)

elif option_site == 'Channel News Asia':
    output_file = os.path.join(data_dir,'cna.json')
    if os.path.isfile(output_file):
        os.remove(output_file)

    # read section file
    with open(os.path.join(data_dir,'cna_sections.txt'),'r') as f:
        sections = f.readlines()[0].split(',')

    # user selection split into two columns
    option_left, option_right = st.columns(2)

    # selector box for section
    option_section = option_left.selectbox(
        'Which section you would like to crawl?',
        [section.capitalize() for section in sections]).lower()

    # selector box for number crawled articles
    option_number_article = option_left.selectbox(
        'How many articles you would like to crawl?',
        [1,2,3,4,5])

    display_options = display_checkboxes(option_right)

st.markdown("***")
crawl_start = st.button('Start crawling')

if crawl_start:
    with st.spinner(f"Crawling {option_number_article} articles ... Please be patient!"):
        scraper = Scraper()
        if option_site == 'Reuters':
            scraper.run_reuters_spiders(
                section=option_section,
                section_category_url=option_section_category_url,
                number_articles=option_number_article
            )
        elif option_site == 'Channel News Asia':
            scraper.run_cna_spiders(
                section=option_section,
                number_articles=option_number_article
            )
        while not os.path.isfile(output_file) or os.path.getsize(output_file) == 0: 
            pass

    st.success('Crawling Done!')

    with st.spinner(f'Preparing file for review ...'):
        results = open_json(output_file)
 
    st.markdown("***")

    st.title('Results')
    for index, article in enumerate(results):
        st.markdown("***")
        st.header(f"Article #{index+1}")

        for display_meta, check in display_options.items():
            if check:
                st.subheader(f"{display_meta.upper()}:")
                if display_meta == 'image':
                    st.image(article[display_meta], width=400)
                    st.write(article[display_meta])
                else:
                    st.write(article[display_meta])
