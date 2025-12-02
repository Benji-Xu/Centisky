; Inno Setup 配置文件 - Centisky 安装程序
; 使用 Inno Setup 6 生成 Windows 安装程序
; 支持自动更新检测

#define MyAppName "Centisky"
#define MyAppVersion "1.1.0"
#define MyAppPublisher "Benji-Xu"
#define MyAppURL "https://github.com/Benji-Xu/Centisky"
#define MyAppExeName "Centisky.exe"
#define SourceDir "program\dist\Centisky"

[Setup]
AppId={{3E5C8B7D-4F2A-4B8C-9E1F-2A3B4C5D6E7F}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}/issues
AppUpdatesURL={#MyAppURL}/releases
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=dist
OutputBaseFilename=Centisky-Setup-{#MyAppVersion}
SetupIconFile=
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64
ArchitecturesAllowed=x64
UninstallDisplayIcon={app}\{#MyAppExeName}
ShowLanguageDialog=no
LanguageDetectionMethod=uilanguage

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 0,6.1

[Files]
; 复制 EXE 和相关文件
Source: "{#SourceDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; 复制模板文件
Source: "templates\*"; DestDir: "{app}\templates"; Flags: ignoreversion recursesubdirs createallsubdirs
; 复制版本文件
Source: "version.txt"; DestDir: "{app}"; Flags: ignoreversion
; 复制更新检查脚本
Source: "program\update_checker.py"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; IconIndex: 0; Comment: "启动 {#MyAppName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"; Comment: "卸载 {#MyAppName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; Tasks: desktopicon; IconIndex: 0; Comment: "启动 {#MyAppName}"
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; Tasks: quicklaunchicon; Comment: "启动 {#MyAppName}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: dirifempty; Name: "{app}\templates"
Type: dirifempty; Name: "{app}"

[Registry]
; 注册应用信息用于控制面板
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#SetupSetting('AppId')}"; ValueType: string; ValueName: "DisplayVersion"; ValueData: "{#MyAppVersion}"
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\Uninstall\{#SetupSetting('AppId')}"; ValueType: string; ValueName: "URLUpdateInfo"; ValueData: "{#MyAppURL}/releases"

[Code]
// 检查 Python 是否已安装
function IsPythonInstalled: Boolean;
var
  ResultCode: Integer;
begin
  Result := False;
  if Exec(ExpandConstant('cmd.exe'), '/c python --version', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) then
  begin
    if ResultCode = 0 then
      Result := True;
  end;
end;

// 初始化安装程序
function InitializeSetup: Boolean;
begin
  Result := True;
  
  // 检查 Python（可选提示）
  if not IsPythonInstalled then
  begin
    MsgBox('未检测到 Python。Centisky 需要 Python 3.7 或更高版本。' + #13#10 +
           '请先从 https://www.python.org 安装 Python。', mbInformation, MB_OK);
  end;
end;
