#!/usr/bin/env python

import imp, os, sys
import logging
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s')


here = os.path.dirname( os.path.abspath( __file__ ) )
chFilePath = os.path.join( os.path.dirname( here ) , "common", "CompileHelper.py" )
try:
  fd = open( chFilePath )
except Exception as e:
  print "Cannot open %s: %s" % ( chFilePath, e )
  sys.exit( 1 )

chModule = imp.load_module( "CompileHelper", fd, chFilePath, ( ".py", "r", imp.PY_SOURCE ) )
fd.close()
chClass = getattr( chModule, "CompileHelper" )

ch = chClass( here )

versions = { 'suds-jurko' : "0.6",
             'boto' : '1.9b' }
ch.setPackageVersions( versions )

for package in versions:
  if not ch.easyInstall( "%s>=%s" % ( package, versions[ package ] ) ):
    logging.error( "Could not deploy %s", package )
    sys.exit( 1 )
