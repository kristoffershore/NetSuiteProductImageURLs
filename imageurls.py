from email.mime import image
import requests
import csv

url_part = '/shop-by-brand/all-products/all-products-14'

url_part = url_part.replace('/', '%2F')

api_url = 'http://suitecommerce.stagelightingstore.com/api/cacheable/items?c=689066&commercecategoryurl=%s&country=US&currency=USD&facet.exclude=custitem_ns_sc_ext_only_pdp%%2Ccustitem_ns_sc_ext_gift_cert_group_id%%2Citemtype&include=facets&language=en&limit=100&fields=itemid,itemimages_detail,itemoptions_detail,storedetaileddescription&n=2&offset=%s&pricelevel=5&sort=itemid&use_pcv=T'

product_list = []

for i in range(0, 40):

    print('Page %s' % (i + 1))

    url = api_url % (url_part, i * 100)

    resp = requests.get(url)

    json_obj = resp.json()

    if len(json_obj['items']) == 0:

            print('No new items, breaking')

            break

    for item in json_obj['items']:
            #print(item,end='\n\n')    
            if len(item['itemimages_detail']) > 0:
                imagedetails = item['itemimages_detail']
        
                cats = list(imagedetails.keys())
                # print(item['itemid'])
                # print(item['itemimages_detail'])
                # print(cats)
                catpath = cats[0]
                product_list.append({

                    'item name/number': item['itemid'],

                    'internal_id': item['internalid'],

                    'has_image': 'T' if len(item['itemimages_detail']) > 0 else 'F',

                    'imgdetails': imagedetails,

                    #'catpath': catpath,
                                    
                    'custitem318(image_url)': imagedetails[catpath]['00.default']['url'] if list(imagedetails[catpath].keys())[0]=='00.default' else (imagedetails[catpath]['url'] if 'url' in list(imagedetails[catpath].keys()) else 'F')
                                
                })
            else:
                product_list.append({

                    'item name/number': item['itemid'],

                    'internal_id': item['internalid'],

                    'has_image': 'T' if len(item['itemimages_detail']) > 0 else 'F',

                    'imgdetails': 'N/A',

                    #'catpath': 'N/A',
                                    
                    'custitem318(image_url)': 'F'

                })
                    
    print('Product count so far: %s' % len(product_list))

    keys = product_list[0].keys()

    with open('image_urls.csv', 'w', newline='') as output_file:

        dict_writer = csv.DictWriter(output_file, keys)

        dict_writer.writeheader()

        dict_writer.writerows([x for x in product_list])
