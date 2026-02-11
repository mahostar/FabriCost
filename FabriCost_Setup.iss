; FabriCost Inno Setup Script
; Creates a professional Windows installer for FabriCost

#define MyAppName "FabriCost"
#define MyAppVersion "1.0"
#define MyAppPublisher "Mahou"
#define MyAppExeName "FabriCost.exe"

[Setup]
; App identification
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; Output settings
OutputDir=installer_output
OutputBaseFilename=FabriCost_Setup_v{#MyAppVersion}

; Icons - use FabriCost icon everywhere
SetupIconFile=FabriCost_Icon.ico
UninstallDisplayIcon={app}\FabriCost_Icon.ico

; Compression
Compression=lzma2/ultra64
SolidCompression=yes

; Appearance
WizardStyle=modern

; Privileges (install for current user by default, no admin needed)
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

; Misc
AllowNoIcons=yes
LicenseFile=
InfoBeforeFile=
InfoAfterFile=

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Copy the entire dist\FabriCost folder contents
Source: "dist\FabriCost\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; Also copy the icon file to the app directory (for uninstall display icon)
Source: "FabriCost_Icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start Menu shortcut with FabriCost icon
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\FabriCost_Icon.ico"

; Desktop shortcut with FabriCost icon
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\FabriCost_Icon.ico"; Tasks: desktopicon

[Run]
; Option to launch app after install
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
