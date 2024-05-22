set PROJECT_DIR=F:\v_yljeyang_v_yljeyang-PC0_v_dev_code\EngineSource\Engine\Source\ThirdParty\PhysX3

cd /d %PROJECT_DIR%
call GenerateProjects_UAT.bat
call RunUAT.bat BuildPhysX -TargetPlatforms=Win64 -TargetConfigs=release+profile+checked -TargetWindowsCompilers=VisualStudio2015 -SkipCreateChangelist