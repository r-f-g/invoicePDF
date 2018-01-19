# invoicePDF
python3 module for create invoice (all language support)

```python3
from invoicePDF import Supplier, Purchaser, Invoice

#load supplier
supplier = Supplier()
supplier.load('TEST')
#load purchaser
purchaser = Purchaser()
purchaser.load('TEST')
#load invoice
invoice = Invoice(supplier)
invoice.load('TEST')

#test A one line data
dataA = [['We are billing you for delivering your material and doing work\n    (SET0001)',1550]]

invoice.create_pdf('testA', '18-0001', purchaser, dataA, True, variablesymbol='180001', constantsymbol='0008', ordernumber='1', \
dateofissuance='19/01/2018', duedate=14, paymentmethod='transfer', creator='Robert Gildein')

#test B with table data
dataB = [['item A', 10, 'pcs', 50], ['item B', 100, 'm', 2.33]]

#also we change final purchaser and notes on invoice
purchaser.finalpurchaser = ['Jozko Mrkvicka', 'Kvetnica 1', '058 01 Poprad']
invoice.notes = 'under Act No. 2'

invoice.create_pdf('testB', '18-0002', purchaser, dataB, True, variablesymbol='180002', constantsymbol='0008', ordernumber='1', \
dateofissuance='19/01/2018', duedate=14, paymentmethod='transfer', creator='Robert Gildein')
```

## editing
All parameters can be stored in folder `.config/` as json file with function `save(name)`. Loading config file is through function `load(fileordata)`, where input can be name of stored config or as variable  `dict`.

If parameters is `None` it will be not print.
### Supplier
It's possible to edit this parameters:
```
name = ''
header = []
info = []
bank = None
SWIFT = None
IBAN = None
tax = 0.2
```
Parameters `header` and `info` are list of lines.

### Purchaser
It's possible to edit this parameters:
```
name = ''
header = []
info = []
finalpurchaser = []
```
Parameters `header`, `info` and `finalpurchaser ` are list of lines.
### Invoice
Basic config for invoice are:

```
font_size = 12
line_spacing = 1.1 #space between two lines
date_format = '%d/%m/%Y'
decimalsep = ','
currency = '€'
path = '' #where file will be stored, possible diffine it in each file name
```

Headers names on invoice:

```
number = 'Ivoice n.' #title in front of invoice number
#
variablesymbol = 'Variable symbol'
constantsymbol = 'Constant symbol'
specificsymbol = 'Specific symbol'
ordernumber = 'Order number'
#title in supplier box
supplier = 'Supplier'
bank = 'Bank'
#title in purchaser and final purchaser box
purchaser = 'Purchaser'
finalpurchaser = 'Final purchaser'
#
dateofissuance = 'Date of issuance'
duedate = 'Due date'
paymentmethod = 'Payment method'
#
textcolumn = 'Description'
quantitycolumn = '#'
unitcolumn = 'Unit'
pricecolumn = 'Price'
taxcolumn = 'Tax'
totalcolumn = 'Total'
#
subtotal = 'Subtotal'
tax = 'Tax'
total = 'Total'
#
creator = 'Issued'
notes = None
invoice footer for signature
took = 'Took'
stamp = 'Stamp'
```
