import sys
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

def parse( data ) :
	parsed_data = []
	m = lambda k : k if k not in mapping else mapping[ k ]
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
						parsed_data.append( ( tag , element.text.strip() ) )
		#for r in parsed_data : print r
	except Exception as e :
		#for i in range( len( data ) ) : print i , data[ i ][ :-1 ]
		print e
	return parsed_data

def export( data , fpath ) :
	#print fpath
	parsed_data = parse( data )
	#for r in parsed_data : print r
	with open( fpath , 'w' ) as f :
		f.write( '<add><doc>\n' )
		for row in parsed_data :
			f.write( '\t<field name = \"%s\">%s</field>\n' % ( row[ 0 ] , row[ 1 ] ) )
		f.write( '</doc></add>\n' )

def split( fpath , counter_start = 0 ) :
	print fpath , counter_start
	xmlpath = '../data/reuters_collection/doc%s.xml'
	counter = counter_start
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
				num = "%s" % counter
				export( sp , xmlpath % num.zfill( 5 ) )
				counter += 1
				sp = []
			else :
				continue

if __name__ == '__main__' :
	fpath = '../raw_data/reut2-000.sgm'
	counter_start = 0
	if len( sys.argv ) > 2 :
		fpath = sys.argv[ 1 ]
		counter_start = int( sys.argv[ 2 ] )
	split( fpath , counter_start )
