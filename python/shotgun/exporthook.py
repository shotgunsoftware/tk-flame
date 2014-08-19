#******************************************************************************
#
# Filename: exportHook.py
#
# Copyright (c) 2014 Autodesk Inc.
# All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# *****************************************************************************

import os
import sys
import sgUtil

def preCustomExport( info, userData ):
   userData[ "shotgunProject" ] = "Flame Sandbox"

   if ( os.environ.get( "DL_SHOTGUN_HOST" ) != None ):
      info[ "destinationHost" ] = os.environ.get( "DL_SHOTGUN_HOST" )

   if ( os.environ.get( "DL_SHOTGUN_PATH" ) != None ):
      info[ "destinationPath" ] = os.environ.get( "DL_SHOTGUN_PATH" )

   if ( os.environ.get( "DL_SHOTGUN_PRESET" ) != None ):
      info[ "presetPath" ] = os.environ.get( "DL_SHOTGUN_PRESET" )

   # Should show window here...

   return ( info, userData )

def postCustomExport( info, userData ):
   return userData


def preExport( info, userData ):
   return ( info, userData )


def postExport( info, userData ):
   return userData


def preExportSequence( info , userData ):
   shotgunProject = userData.get( "shotgunProject" )
   if ( shotgunProject != "" ):
     sequenceName = info.get( "sequenceName" )
     sgUtil.createSequence( projectName = shotgunProject,
                            sequenceName = sequenceName ),

   return ( info, userData )


def postExportSequence( info, userData ):
   return ( userData )


def preExportAsset( info, userData ):
   shotgunProject   = userData.get( "shotgunProject" )
   shotName         = info.get( "shotName" )
   if ( shotgunProject != "" and shotName != "" ):
      sequenceName  = info.get( "sequenceName" )
      assetName     = info.get( "assetName" )

      sgUtil.createShotIfDoesntExist( projectName = shotgunProject,
                                      shotName = shotName )
      sgUtil.linkShotToSequence( projectName = shotgunProject,
                                 sequenceName = sequenceName,
                                 shotName = shotName )
      sgUtil.createAsset( projectName = shotgunProject,
                          assetName = assetName )
      sgUtil.linkAssetToShot( projectName = shotgunProject,
                              assetName = assetName,
                              shotName = shotName )

   return ( info, userData )


def postExportAsset( info, userData ):
   shotgunProject   = userData.get( "shotgunProject" )
   shotName         = info.get( "shotName" )
   if ( shotgunProject != "" and shotName != "" ):
      shotName         = info.get( "shotName" )
      assetType        = info.get( "assetType" )
      destinationPath  = info.get( "destinationPath" )
      resolvedPath     = info.get( "resolvedPath" )

      if ( assetType == 'video' ):
         imageFile = os.path.join( destinationPath, resolvedPath )
         try:
            start = imageFile.rindex( '[' )
            sep = imageFile.rindex( '-' )
            end = imageFile.rindex( '[' )
            imageFile = imageFile[ : start - 1 ] \
                      + imageFile[ start : sep - 1 ] \
                      + imageFile[ end : ]
         except:
            pass
         sgUtil.uploadThumbnail( projectName = shotgunProject,
                                 shotName = shotName,
                                 imageFile = imageFile )
   return ( userData )


def useBackburnerPostExportAsset():
   return True


def getCustomExportName():
   return "Create Shotgun Sequence"


if ( __name__ == "__main__" ):
   import sys
   import ast

   # Call a hook from the command line:
   #
   #  exportHook.py <function> <args>
   #
   method = sys.argv[ 1 ]
   params = ( ast.literal_eval( p ) for p in sys.argv[ 2: ] )
   globals()[ method ]( * params )
