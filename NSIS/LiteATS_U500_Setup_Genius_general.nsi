;LiteATS U500 Setup Script
;Start Menu Folder Selection Included
;Written by Benjamin ZERATH

;--------------------------------
;Include Modern UI

  !include "MUI2.nsh"

;--------------------------------
;General

  ;Name and file
  
  Name "LiteATS U500 v1.2"
  OutFile "Setup LiteATS U500 v1.2.exe"


  ;Default installation folder
  InstallDir "$PROGRAMFILES\Alstom Transport\LiteATS U500 v1.2"

  ;Get installation folder from registry if available
  InstallDirRegKey HKCU "Software\Alstom Transport\LiteATS U500 v1.2" ""

  ;Request application privileges for Windows Vista
  RequestExecutionLevel admin

;--------------------------------
;Variables

  Var StartMenuFolder

;--------------------------------
;Interface Settings

  !define MUI_ABORTWARNING



;--------------------------------
;Pages

  !insertmacro MUI_PAGE_WELCOME
  !insertmacro MUI_PAGE_LICENSE ".\Copyright.txt"
  !insertmacro MUI_PAGE_COMPONENTS
  !insertmacro MUI_PAGE_DIRECTORY

  ;Start Menu Folder Page Configuration
  !define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKCU"
  !define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\Alstom Transport\LiteATS U500 v1.2"
  !define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"

  !insertmacro MUI_PAGE_STARTMENU Application $StartMenuFolder

  !insertmacro MUI_PAGE_INSTFILES
  !insertmacro MUI_PAGE_FINISH



  !insertmacro MUI_UNPAGE_WELCOME
  !insertmacro MUI_UNPAGE_COMPONENTS
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES
  !insertmacro MUI_UNPAGE_FINISH

;--------------------------------
;Languages

  !insertmacro MUI_LANGUAGE "English"

;--------------------------------
;Installer Sections

Section "Main" Main

  SetOutPath "$INSTDIR"

  ;ADD YOUR OWN FILES HERE...
  File /r "..\Clean\dist\*"

  ;Store installation folder
  WriteRegStr HKCU "Software\Alstom Transport\LiteATS U500 v1.2" "" $INSTDIR

  ;Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"

  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\LiteATS U500 v1.2" \
                 "DisplayName" "LiteATS U500 v1.2"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\LiteATS U500 v1.2" \
                 "UninstallString" "$\"$INSTDIR\Uninstall.exe$\""

  !insertmacro MUI_STARTMENU_WRITE_BEGIN Application

  ;Create shortcuts
  CreateDirectory "$SMPROGRAMS\$StartMenuFolder"
  CreateShortCut "$SMPROGRAMS\$StartMenuFolder\Uninstall.lnk" "$INSTDIR\Uninstall.exe"

  !insertmacro MUI_STARTMENU_WRITE_END


SectionEnd

Section "StartMenu Shortcut" StartMenu_SHORTCUT
  SetOutPath "$INSTDIR"
  CreateShortCut "$SMPROGRAMS\$StartMenuFolder\LiteATS U500 v1.2.lnk" "$INSTDIR\LiteATS_U500.exe" ""
SectionEnd


Section "Desktop Shortcut" Desktop_SHORTCUT
  SetOutPath "$INSTDIR"
  CreateShortcut "$DESKTOP\LiteATS U500 v1.2.lnk" "$INSTDIR\LiteATS_U500.exe" ""
SectionEnd

;--------------------------------
;Uninstaller Section

Section "Un.Application" Application

  ;Delete Files
  Delete "$INSTDIR\dist\*"
  Delete "$INSTDIR\*"
  RMDir /r "$INSTDIR\dist\Xml"
  RMDir /r "$INSTDIR\dist\tcl"
  RMDir /r "$INSTDIR\dist\Extra"


  ;Remove the installation directory
   RMDir /r "$INSTDIR"

  !insertmacro MUI_STARTMENU_GETFOLDER Application $StartMenuFolder

  Delete "$DESKTOP\LiteATS U500 v1.2.lnk"
  Delete "$SMPROGRAMS\$StartMenuFolder\Uninstall.lnk"
  Delete "$SMPROGRAMS\$StartMenuFolder\LiteATS U500 v1.2.lnk"
  RMDir "$SMPROGRAMS\$StartMenuFolder"

  DeleteRegKey /ifempty HKCU "Software\Alstom Transport\LiteATS U500 v1.2"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\LiteATS U500 v1.2"
SectionEnd


;Section "Un.UserData" UserData
;
  ;Delete Files
;  RMDir /r "$INSTDIR\dist\Data"
;  RMDir /r "$INSTDIR\dist\Projects"
;  RMDir /r "$INSTDIR\dist\Recordings"

;SectionEnd

;--------------------------------
;Descriptions

  ;Language strings
  LangString DESC_Sec_StartMenu_SHORTCUT ${LANG_ENGLISH} "Add a shortcut in the Start Menu."
  LangString DESC_Sec_Desktop_SHORTCUT ${LANG_ENGLISH} "Add a shortcut on the Desktop."
  LangString DESC_Sec_Main ${LANG_ENGLISH} "This is the main part of application, a configuration file is included."
  LangString DESC_Sec_Application ${LANG_ENGLISH} "Uninstall the application."

  ;Assign language strings to install sections
  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN

  !insertmacro MUI_DESCRIPTION_TEXT ${Main} $(DESC_Sec_Main)
  !insertmacro MUI_DESCRIPTION_TEXT ${StartMenu_SHORTCUT} $(DESC_Sec_StartMenu_SHORTCUT)
  !insertmacro MUI_DESCRIPTION_TEXT ${Desktop_SHORTCUT} $(DESC_Sec_Desktop_SHORTCUT)

  !insertmacro MUI_FUNCTION_DESCRIPTION_END

  ;Assign language strings to install sections
  !insertmacro MUI_UNFUNCTION_DESCRIPTION_BEGIN

  !insertmacro MUI_DESCRIPTION_TEXT ${Application} $(DESC_Sec_Application)
;  !insertmacro MUI_DESCRIPTION_TEXT ${UserData} $(DESC_Sec_UserData)

  !insertmacro MUI_UNFUNCTION_DESCRIPTION_END




Var UNINSTALL_PROG

Function .onInit
  ClearErrors
  ReadRegStr $UNINSTALL_PROG HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\LiteATS U500 v1.2" "UninstallString"
  IfErrors install

  MessageBox MB_YESNO|MB_ICONQUESTION \
    "LiteATS U500 v1.2 is already installed in your computer. \
	$\nClick yes to force the install process, click no to abort." \
      /SD IDYES \
      IDYES install \
      IDNO done
  Abort
  
done:
  Abort
  
install:

  
FunctionEnd



