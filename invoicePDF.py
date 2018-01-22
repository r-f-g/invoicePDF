from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import datetime
import json
from io import BytesIO
import os
PATH = os.path.dirname(os.path.abspath(__file__))

pdfmetrics.registerFont(TTFont('DejaVuSans',PATH+'/.fonts/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold',PATH+'/.fonts/DejaVuSans-Bold.ttf'))

class Supplier:
	def __init__(self, **kwargs):
		self.name = ''
		self.header = []
		self.info = []
		self.bank = None
		self.SWIFT = None
		self.IBAN = None
		self.tax = 0.2
		self.__dict__.update((k, v) for k, v in kwargs.items() if k in self.__dict__.keys())

	def save(self, to):
		with open(PATH+'/.cofig/supplier_{0}.json'.format(to), 'w') as f:
			json.dump(self.__dict__, f, ensure_ascii=False)

	def load(self, fileordata):
		if type(fileordata) == str:
			with open(PATH+'/.cofig/supplier_{0}.json'.format(fileordata), 'r', encoding='utf-8') as f:
				self.__dict__.update((k, v) for k,v in json.loads(f.read()).items())
		else:
			self.__dict__.update((k, v) for k,v in fileordata)
		
class Purchaser:
	def __init__(self, **kwargs):
		self.name = ''
		self.header = []
		self.info = []
		self.finalpurchaser = []
		self.__dict__.update((k, v) for k, v in kwargs.items() if k in self.__dict__.keys())

	def save(self, to):
		with open(PATH+'/.cofig/purchaser_{0}.json'.format(to), 'w') as f:
			json.dump(self.__dict__, f, ensure_ascii=False)

	def load(self, fileordata):
		if type(fileordata) == str:
			with open(PATH+'/.cofig/purchaser_{0}.json'.format(fileordata), 'r', encoding='utf-8') as f:
				self.__dict__.update((k, v) for k,v in json.loads(f.read()).items())
		else:
			self.__dict__.update((k, v) for k,v in fileordata)

class Invoice:
	def __init__(self, supplier, **kwargs):
		self.__supplier = supplier
		#
		self.font_size = 12
		self.line_spacing = 1.1
		self.date_format = '%d/%m/%Y'
		self.decimalsep = ','
		self.currency = '€'
		self.path = ''
		#
		self.number = 'Ivoice n.'
		#
		self.variablesymbol = 'Variable symbol'
		self.constantsymbol = 'Constant symbol'
		self.specificsymbol = 'Specific symbol'
		self.ordernumber = 'Order number'
		#
		self.supplier = 'Supplier'
		self.bank = 'Bank'
		#
		self.purchaser = 'Purchaser'
		self.finalpurchaser = 'Final purchaser'
		#
		self.dateofissuance = 'Date of issuance'
		self.duedate = 'Due date'
		self.paymentmethod = 'Payment method'
		#
		self.textcolumn = 'Description'
		self.quantitycolumn = '#'
		self.unitcolumn = 'Unit'
		self.pricecolumn = 'Price'
		self.taxcolumn = 'Tax'
		self.totalcolumn = 'Total'
		#
		self.subtotal = 'Subtotal'
		self.tax = 'Tax'
		self.total = 'Total'
		#
		self.creator = 'Issued'
		self.notes = None
		#
		self.took = 'Took'
		self.stamp = 'Stamp'
		#
		self.__dict__.update((k, v) for k, v in kwargs.items() if k in self.__dict__.keys())

	def save(self, to):
		out = {k:v for k, v in self.__dict__.items() if k.find('__') == -1}
		with open(PATH+'/.cofig/invoice_{0}.json'.format(to), 'w') as f:
			json.dump(out, f, ensure_ascii=False)

	def load(self, fileordata):
		if type(fileordata) == str:
			with open(PATH+'/.cofig/invoice_{0}.json'.format(fileordata), 'r', encoding='utf-8') as f:
				self.__dict__.update((k, v) for k,v in json.loads(f.read()).items())
		else:
			self.__dict__.update((k, v) for k,v in fileordata)

	def __float(self, number):
		if self.decimalsep == ',':
			return '{0:,.2f}'.format(number).replace(',',' ').replace('.',',')
		else:
			return '{0:,.2f}'.format(number)

	def __currency(self, number):
		if self.decimalsep == ',':
			return '{0:,.2f} {1}'.format(number, self.currency).replace(',',' ').replace('.',',')
		else:
			return '{0:,.2f} {1}'.format(number, self.currency)

	def __drawFrame(self, top=1*cm):
		self.__c.saveState()
		self.__c.setLineWidth(.01*cm)
		self.__c.rect(1*cm,1.5*cm,A4[0]-2*cm,A4[1]-(top+1.5*cm), stroke=1, fill=0)
		self.__c.restoreState()
		
	def __drawHeader(self):
		self.__c.saveState()
		self.__c.setLineWidth(.01*cm)
		self.__c.rect(1*cm,A4[1]*0.6,A4[0]-2*cm,A4[1]*0.4-1.5*cm, stroke=1, fill=0)
		self.__c.rect(1*cm,A4[1]-7.5*cm,10*cm,6*cm, stroke=1, fill=0)
		self.__c.rect(11*cm,A4[1]-3.5*cm,A4[0]-12*cm,2*cm, stroke=1, fill=0)
		self.__c.rect(11*cm,A4[1]-9.5*cm,A4[0]-12*cm,8*cm, stroke=1, fill=0)
		self.__c.rect(1*cm,A4[1]*0.6,10*cm,A4[1]*0.4-9.5*cm, stroke=1, fill=0)
		self.__c.setLineWidth(.05*cm)
		self.__c.rect(1*cm,A4[1]-9.5*cm,10*cm,2*cm, stroke=1, fill=0)
		self.__c.rect(11*cm,A4[1]-9.5*cm,A4[0]-12*cm,6*cm, stroke=1, fill=0)
		self.__c.restoreState()

	def __drawFooter(self, kwargs):
		if self.__page < len(self.__pageBreak):
			self.__break()
		self.__c.saveState()
		self.__c.setLineWidth(.01*cm)
		self.__c.rect(1*cm,1.5*cm,A4[0]/2-1*cm,2*cm, stroke=1, fill=0)
		self.__c.rect(A4[0]/2,1.5*cm,A4[0]/2-1*cm,2*cm, stroke=1, fill=0)
		self.__c.setLineWidth(.01*cm)
		self.__c.setDash([3,1],1)
		y = 1.7*cm+self.font_size
		self.__c.line(A4[0]/4 - 2.5*cm,y,A4[0]/4 + 2.5*cm,y)
		self.__c.line(3*A4[0]/4 - 2.5*cm,y,3*A4[0]/4 + 2.5*cm,y)
		self.__c.setFont("DejaVuSans", self.font_size)
		self.__c.drawCentredString(A4[0]/4, 1.6*cm, self.took)
		self.__c.drawCentredString(3*A4[0]/4, 1.6*cm, self.stamp)
		x, y = 2*cm, 4.8*cm
		y = self.__drawIF(x, y, self.__p(kwargs, 'creator'), self.creator, 2.5*cm)
		y = self.__drawIF(x, y, self.__p(kwargs, 'creator_email'), '', 2.5*cm)
		self.__c.setFont("DejaVuSans", round(self.font_size*0.5))
		if self.notes != None:
			for row in self.notes.split('\n'):
				y = self.__drawIF(x, y, row,font_resize=0.5)
		self.__c.restoreState()

	def __drawPageNumber(self):
		self.__c.saveState()
		self.__c.drawCentredString(A4[0]/2,1*cm, '{0}/{1}'.format(self.__page, len(self.__pageBreak)))
		self.__c.restoreState()

	def __drawInvoice(self, number, kwargs):
		self.__c.saveState()
		self.__c.setFont("DejaVuSans-Bold", round(self.font_size*1.35))
		self.__c.drawString(1.2*cm, A4[1]-1.3*cm, self.__supplier.name)
		self.__c.drawRightString(A4[0]-1.2*cm, A4[1]-1.3*cm, '{0}: {1}'.format(self.number, number))
		self.__c.setFont("DejaVuSans", round(self.font_size*0.8))
		x, y = 11.5*cm, A4[1]-2*cm
		y = self.__drawIF(x, y, self.__p(kwargs, 'variablesymbol'), self.variablesymbol, A4[0]-13*cm, .8, 'R')
		y = self.__drawIF(x, y, self.__p(kwargs, 'constantsymbol'), self.constantsymbol, A4[0]-13*cm, .8, 'R')
		y = self.__drawIF(x, y, self.__p(kwargs, 'specificsymbol'), self.specificsymbol, A4[0]-13*cm, .8, 'R')
		y = self.__drawIF(x, y, self.__p(kwargs, 'ordernumber'), self.ordernumber, A4[0]-13*cm, .8, 'R')
		self.__c.setFont("DejaVuSans", self.font_size)
		x, y = 1.5*cm, A4[1]-10.4*cm
		date = datetime.datetime.now() if self.__p(kwargs, 'dateofissuance') == None else self.__p(kwargs, 'dateofissuance')
		if type(date) == str: date = datetime.datetime.strptime(date, self.date_format)
		duedate = self.__p(kwargs, 'duedate')
		if duedate == None:
			duedate = date + datetime.timedelta(days=14)
		elif type(duedate) == int:
			duedate = date + datetime.timedelta(days=duedate)
		elif type(duedate) == str:
			duedate = datetime.datetime.strptime(duedate, self.date_format)
		y = self.__drawIF(x, y, date.strftime(self.date_format), self.dateofissuance, 6*cm)
		y = self.__drawIF(x, y, duedate.strftime(self.date_format), self.duedate, 6*cm)
		y = self.__drawIF(x, y, self.__p(kwargs, 'paymentmethod'), self.paymentmethod, 6*cm)
		self.__c.restoreState()

	def __drawInfo(self, obj, x, y, title):
		self.__c.saveState()
		self.__c.setFont("DejaVuSans", self.font_size)
		if title != None: self.__c.drawString(x-.8*cm, y+.6*cm, '{0}:'.format(title))
		self.__c.setFont("DejaVuSans-Bold", self.font_size*1.2)
		for header in obj.header:
			y = self.__drawIF(x, y, header, font_resize=1.2)
		y -= self.font_size*1.2*self.line_spacing
		self.__c.setFont("DejaVuSans", self.font_size)
		for info in obj.info:
			h0 = info.split(':')
			if len(h0) == 2:
				y = self.__drawIF(x, y, h0[1], h0[0], 2*cm)
			else:
				y = self.__drawIF(x, y, info)
		self.__c.restoreState()

	def __drawSupplier(self):
		self.__c.saveState()
		self.__drawInfo(self.__supplier, 2*cm, A4[1]-2.5*cm, self.supplier)
		self.__c.setFont("DejaVuSans", round(self.font_size*.9))
		x, y = 1.5*cm, A4[1]-8.2*cm
		y = self.__drawIF(x, y, self.__supplier.bank, self.bank, 2*cm, .9)
		y = self.__drawIF(x, y, self.__supplier.SWIFT, 'SWIFT', 2*cm, .9)
		y = self.__drawIF(x, y, self.__supplier.IBAN, 'IBAN', 2*cm, .9)
		self.__c.restoreState()

	def __drawPurchaser(self):
		self.__c.saveState()
		self.__drawInfo(self.__purchaser, 12*cm, A4[1]-4.5*cm, self.purchaser)
		if self.__purchaser.finalpurchaser != []:
			self.__c.setFont("DejaVuSans", round(self.font_size*.9))
			x, y = 11.2*cm, A4[1]-10*cm
			if self.finalpurchaser != None: y = self.__drawIF(x, y, '{0}:'.format(self.finalpurchaser), font_resize=.9)
			x = 12*cm
			for info in self.__purchaser.finalpurchaser:
				y = self.__drawIF(x, y, info, font_resize=.9)
		self.__c.restoreState()
		
	def __drawIF(self, x, y, text, title=None, width=0, font_resize=1, option='L'):
		if title != None and text != None:
			if option == 'L':
				self.__c.drawString(x, y, '{0}:'.format(title) if title != '' else '')
				self.__c.drawString(x+width, y, text)
			elif option == 'R':
				self.__c.drawString(x, y, '{0}:'.format(title) if title != '' else '')
				self.__c.drawRightString(x+width, y, text)
			y -= font_resize*self.font_size*self.line_spacing
		elif text != None:
			self.__c.drawString(x, y, text)
			y -= font_resize*self.font_size*self.line_spacing
		return y
	
	def __p(self, dic, key):
		try:
			return dic[key]
		except:
			return None
		
	def __drawLine(self, line, size, y):
		self.__c.saveState()
		for i, col in enumerate(line):
			self.__c.drawString(2*cm+sum(size[:i]), y, col) if i==0 else self.__c.drawRightString(2*cm+sum(size[:i]), y, col)
		self.__c.restoreState()

	def __break(self):
		self.__c.showPage()
		self.__drawFrame()
		self.__page += 1
		self.__drawPageNumber()
		
	def __drawTable(self, data, size, tax):
		y = A4[1]*.6 - 1*cm
		#title
		self.__c.setFont("DejaVuSans-Bold", round(self.font_size*.8))
		self.__c.setLineWidth(.03*cm)
		self.__c.line(1.5*cm,y-5,19.5*cm,y-5)
		self.__drawLine(data[0], size, y)
		y -= self.font_size*self.line_spacing + .3*cm
		#body
		self.__c.setFont("DejaVuSans", round(self.font_size*.8))
		for i, d in enumerate(data[1:-(3 if tax else 1)]):
			if sum(self.__pageBreak[:self.__page]) <= i:
				self.__break()
				y = A4[1]-2*cm
			self.__c.setLineWidth(.001*cm)
			self.__c.line(1.5*cm,y-2,19.5*cm,y-2)
			self.__drawLine(d, size, y)
			y -= self.font_size*self.line_spacing
		#footer
		if sum(self.__pageBreak[:self.__page]) - len(data[1:-(3 if tax else 1)]) <= 4:
			self.__break()
			y = A4[1]-2*cm
		self.__c.setFont("DejaVuSans-Bold", round(self.font_size*.8))
		for d in data[-(3 if tax else 1):]:
			self.__drawLine(d, size, y)
			y -= self.font_size*self.line_spacing

	def __drawNoTable(self, data, tax):
		self.__c.saveState()
		y = A4[1]*.6 - 1*cm
		self.__c.setFont("DejaVuSans", self.font_size)
		for line in data[0][0].split('\n'):
			self.__c.drawString(2*cm, y, line)
			y -= self.font_size*self.line_spacing
		self.__c.setFont("DejaVuSans-Bold", self.font_size)
		if tax:
			y = self.__drawIF(13*cm, y, self.__currency(data[0][1]), self.subtotal, width=6*cm, option='R')
			y = self.__drawIF(13*cm, y, self.__currency(data[0][1]*self.__supplier.tax), self.tax, width=6*cm, option='R')
			y = self.__drawIF(13*cm, y, self.__currency(data[0][1]*(1+self.__supplier.tax)), self.total, width=6*cm, option='R')
		else:
			y = self.__drawIF(13*cm, y, self.__currency(data[0][1]), self.total, width=6*cm, option='R')
		self.__c.restoreState()

	def __getTable(self, data, tax):
		out = []
		total = [0, 0, 0]
		if tax:
			size = [6*cm, 2*cm, 2.5*cm, 2.5*cm, 4*cm]
			headers = ['textcolumn', 'quantitycolumn', 'unitcolumn', 'pricecolumn', 'taxcolumn', 'totalcolumn']
			out.append([self.__dict__[h] for h in headers])
			for d in data:
				out.append([d[0], '{:.0f}'.format(d[1]), d[2], self.__float(d[3]), self.__float(d[3]*self.__supplier.tax), \
						self.__float(d[1]*d[3]*(1+self.__supplier.tax))])
				total[0] += d[1]*d[3]
				total[1] += d[1]*d[3]*self.__supplier.tax
				total[2] += d[1]*d[3]*(1+self.__supplier.tax)
			out.append(['','','',self.subtotal, '', self.__currency(total[0])])
			out.append(['','','',self.tax, '', self.__currency(total[1])])
			out.append(['','','',self.total, '', self.__currency(total[2])])
		else:
			size = [8.5*cm, 2*cm, 2.5*cm, 4*cm]
			headers = ['textcolumn', 'quantitycolumn', 'unitcolumn', 'pricecolumn', 'totalcolumn']
			out.append([self.__dict__[h] for h in headers])
			for d in data:
				out.append([d[0], '{:.0f}'.format(d[1]), d[2], self.__float(d[3]), self.__float(d[1]*d[3])])
				total[2] += d[1]*d[3]
			out.append(['','',self.total, '', self.__currency(total[2])])
		return out, size

	def __getPageBrake(self, data):
		first = int((A4[1]*.6-3.5*cm)/(self.font_size*self.line_spacing))
		empty = int((A4[1]-2.5*cm)/(self.font_size*self.line_spacing))
		last = int((A4[1]-6.5*cm)/(self.font_size*self.line_spacing))
		out = [first]
		while sum(out) <= len(data):
			out.append(empty)
		if sum(out) - len(data) <= 9:
			out.append(last)
		return out

	def __build(self, number, Purchaser, data, tax, kwargs):
		self.__purchaser = Purchaser
		self.__drawFrame(top=1.5*cm)
		self.__drawHeader()
		self.__drawInvoice(number, kwargs)
		self.__drawSupplier()
		self.__drawPurchaser()
		self.__pageBreak = self.__getPageBrake(data)
		self.__page = 1
		self.__drawPageNumber()
		if len(data) == 1 and len(data[0]) == 2:
			self.__drawNoTable(data, tax)
		else:
			table, size = self.__getTable(data, tax)
			self.__drawTable(table, size, tax)
		self.__drawFooter(kwargs)
		self.__c.save()

	def create_pdf(self, name, number, Purchaser, data, tax, **kwargs):
		self.__c = canvas.Canvas(self.path+name+".pdf")
		self.__build(number, Purchaser, data, tax, kwargs)
		

	def return_pdf(self, number, Purchaser, data, tax, **kwargs):
		buffer = BytesIO()
		self.__c = canvas.Canvas(buffer)
		self.__build(number, Purchaser, data, tax, kwargs)
		pdf = buffer.getvalue()
		buffer.close()
		return pdf