#******************************************************************************
#
# Filename: sgUtil.py
#
# Copyright (c) 2014 Autodesk Inc.
# All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# *****************************************************************************

#!/bin/env python
from shotgun_api3 import *
import sys

SG_SERVER   = "https://xxxxx-xxxx.shotgunstudio.com"
SG_APP_KEY  = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
SG_APP      = "xxxxx-xxxx"
sg          = Shotgun( SG_SERVER, SG_APP, SG_APP_KEY )

def getProject( projectName ):
   """
   Returns a project information
   """
   return sg.find_one( 'Project',
                       filters = [ [ "name", "is", projectName ] ] )

def getSomethingInProject( projectName, attribute, attributeName, fields ):
   """
   Returns an attribute information
   """
   project = getProject( projectName )
   return sg.find_one( attribute,
                       filters = [ [ 'code', 'is', attributeName ],
                                   [ 'project', 'is', { 'type': 'Project',
                                                        'id': project[ 'id' ] } ] ],
                       fields = fields )

def getSequence( projectName, sequenceName, fields = [ 'id' ] ):
   """
   Returns a sequence information
   """
   return getSomethingInProject( projectName, "Sequence", sequenceName, fields )

def getShot( projectName, shotName, fields = [ 'id' ] ):
   """
   Returns a shot information
   """
   return getSomethingInProject( projectName, "Shot", shotName, fields )

def getAsset( projectName, assetName, fields = [ 'id' ] ):
   """
   Returns an asset information
   """
   return getSomethingInProject( projectName, "Asset", assetName, fields )

def createShot( projectName, shotName ):
   """
   Create a shot with a project name and a shot name
   """

   project = getProject( projectName )
   return sg.create( 'Shot', { 'code': shotName, 'project': project } )

def createShotIfDoesntExist( projectName, shotName ):
   """
   Create a shot if it doesn't exist
   If it exists, simply return the already existing one
   """

   shot = getShot( projectName, shotName )
   if not shot:
      shot = createShot( projectName, shotName )
   return shot

def createSequence( projectName, sequenceName ):
   """
   Create a sequence with a project name and a shot name
   """

   project = getProject( projectName )
   return sg.create( 'Sequence', { 'code': sequenceName, 'project': project } )

def createAsset( projectName, assetName ):
   """
   Create a sequence with a project name and a shot name
   """

   project = getProject( projectName )
   shot = sg.create( 'Asset', { 'code': assetName, 'project': project } )
   return shot

def linkAssetToShot( projectName, assetName, shotName ):
   """
   Link an asset to the specified shot, by name
   """
   shot = getShot( projectName, shotName )
   asset = getAsset( projectName, assetName,
                     fields = [ 'id', 'shots' ] )
   shots = asset[ "shots" ]
   found = False
   for s in shots:
      if ( shot[ 'id' ] == s[ 'id' ] ):
         found = True
         break
   if ( not found ):
      shots.append( shot )
      asset = sg.update( 'Asset', asset[ 'id' ], { 'shots' : shots } )

def linkAssetToSequence( projectName, assetName, sequenceName ):
   """
   Link an asset to the specified sequence, by name
   """
   sequence = getSequence( projectName, sequenceName )
   asset = getAsset( projectName, assetName,
                     fields = [ 'id', 'sequences' ] )
   sequences = asset[ "sequences" ]
   found = False
   for s in sequences:
      if ( sequence[ 'id' ] == s[ 'id' ] ):
         found = True
         break
   if ( not found ):
      sequences.append( sequence )
      asset = sg.update( 'Asset', asset[ 'id' ], { 'sequences' : sequences } )

def linkShotToSequence( projectName, sequenceName, shotName ):
   """
   Link a Shot to a specified sequence, by name
   """

   shot = getShot( projectName, shotName )
   sequence = getSequence( projectName, sequenceName )
   return sg.update( 'Shot', shot[ 'id' ], { 'sg_sequence' : sequence } )

def uploadThumbnail( projectName, shotName, imageFile ):
   shot = getShot( projectName, shotName )
   return sg.upload_thumbnail( 'Shot', shot[ 'id' ], imageFile )
