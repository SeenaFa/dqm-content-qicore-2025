REM create test directories for each measure resource
for %%a in (input\resources\measure\*.json) do md input\tests\measure\%%~na

REM run _extractBundleResources on each measure test directory
for /d %%a in (input\tests\measure\*.*) do _extractBundleResources %%a
