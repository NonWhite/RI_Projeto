import sys
from copy import deepcopy as copy
import xml.etree.ElementTree as ET

not_allowed_fields = [ 'UNKNOWN' ]
mapping = {
	'TITLE' : 'titulo' ,
	'BODY' : 'content'
}

def is_start( line ) :
	return line.find( '<REUTERS' ) == 0

def is_end( line ) :
	return line.find( '</REUTERS' ) == 0

def parse( data , num_doc ) :
	parsed_data = []
	m = lambda k : k.lower() if k not in mapping else mapping[ k ]
	try :
		root = ET.fromstring( ''.join( data ) )
		for element in root :
			tag = element.tag
			children = element.getchildren()
			if len( children ) > 0 :
				for ch in element :
					if ch.tag == 'D' :
						if tag not in not_allowed_fields :
							parsed_data.append( ( m( tag ) , ch.text.strip() ) )
					else :
						if tag not in not_allowed_fields :
							parsed_data.append( ( m( ch.tag ) , ch.text.strip() ) )
			else :
				if element.text :
					if tag not in not_allowed_fields :
						parsed_data.append( ( m( tag ) , element.text.strip() ) )
		parsed_data.append( ( 'id' , num_doc ) )
	except Exception as e :
		print e
	return parsed_data

def split( fpath , counter_start = 0 ) :
	print fpath , counter_start
	docs = []
	with open( fpath , 'r' ) as f :
		first_line = True
		sp = []
		for line in f :
			if first_line :
				first_line = False
				continue
			sp.append( line )
			if is_start( line ) :
				continue
			elif is_end( line ) :
				docs.append( copy( sp ) )
				sp = []
			else :
				continue
	
	xmlpath = '../data/reuters_collection/doc%s.xml' % ( "%s" % ( counter_start / 1000 ) ).zfill( 2 )
	num_doc = counter_start
	with open( xmlpath , 'w' ) as f :
		f.write( "<add>\n" )
		for d in docs :
			parsed_data = parse( d , num_doc )
			f.write( '\t<doc>\n' )
			for row in parsed_data :
				f.write( '\t\t<field name = \"%s\">%s</field>\n' % ( row[ 0 ] , row[ 1 ] ) )
			f.write( '\t</doc>\n' )
			num_doc += 1
		f.write( "</add>\n" )

if __name__ == '__main__' :
	fpath = '../raw_data/reut2-000.sgm'
	counter_start = 0
	if len( sys.argv ) > 2 :
		fpath = sys.argv[ 1 ]
		counter_start = int( sys.argv[ 2 ] )
	split( fpath , counter_start )
