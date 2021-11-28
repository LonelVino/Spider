
from scrapy import Item, Field

'''
Spider of Scarpy returns each extracted data as items.
Item Types: Dictionaries or `Item`

`Item`: replicate the standard **dict** API, allows defining `field` names
`Field`: used to specify **metadata** for each field

- You can initialize by `classItem = Class(key1=..., key2=....)`
- You can get the field values by `classItem[key]` or  `classItem.egt(key)`  
- You can just use the typical dict API to access all values by `classItem.keys()` and  `classItem.items()`
'''

class ErrorItem(Item):
    uid = Field()
    url = Field()
