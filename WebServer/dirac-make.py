#!/usr/bin/env python

import imp
import os
import sys
import urllib
import logging
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s')


here = os.path.dirname( os.path.abspath( __file__ ) )
chFilePath = os.path.join( os.path.dirname( here ) , "common", "CompileHelper.py" )
try:
  with open( chFilePath ) as fd:
    chModule = imp.load_module( "CompileHelper", fd, chFilePath, ( ".py", "r", imp.PY_SOURCE ) )
except Exception as e:
  print "Cannot open %s: %s" % ( chFilePath, e )
  sys.exit( 1 )

chClass = getattr( chModule, "CompileHelper" )

ch = chClass( here )

versions = { 'pcre' : "8.01",
             'lighttpd' : '1.4.28' }
ch.setPackageVersions( versions )

lighttpdFile = "lighttpd-%s.tar.bz2" % versions[ 'lighttpd' ]
lighttpdFilePath = os.path.join( here, lighttpdFile )
if not os.path.isfile( lighttpdFilePath ):
  try:
    urllib.urlretrieve( "http://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-%s.tar.bz2" % versions[ 'lighttpd' ],
                        lighttpdFilePath )
  except Exception as e:
    logging.error( "Could not retrieve lighttpd %s: %s" % ( versions[ 'lighttpd' ], e ) )
    sys.exit( 1 )

if not ch.deployPackage( 'pcre' ):
  logging.error( "Could not deploy pcre" )
  sys.exit( 1 )

prefix = ch.getPrefix()
configArgs = []
configArgs.append( '--with-openssl-includes="%s"' % os.path.join( prefix, "include" ) )
configArgs.append( '--with-openssl-libs="%s"' % os.path.join( prefix, "lib" ) )
configArgs.append( '--with-openssl' )

env = { 'PATH' : '%s:%s' % ( os.path.join( ch.getPrefix(), 'bin' ), os.environ[ 'PATH' ] ) }
ch.setDefaultEnv( env )
if not ch.deployPackage( 'lighttpd', configureArgs = " ".join( configArgs ) ):
  logging.error( "Could not deploy lighttpd" )
  sys.exit( 1 )

ch.copyPostInstall()
