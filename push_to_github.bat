@echo off
chcp 65001 > nul
echo ======================================================================
echo    ربط المشروع بحساب GitHub للنشر على Render.com
echo ======================================================================
echo.
echo 1. افتح الرابط التالي وأنشئ مستودعاً جديداً (New Repository):
echo    https://github.com/new
echo.
echo 2. بعد إنشاء المستودع، انسخ رابطه (مثال: https://github.com/username/repo.git)
echo.
set /p REPO_URL="الصق رابط مستودع GitHub هنا: "

if "%REPO_URL%"=="" (
    echo لم يتم إدخال الرابط. تم إلغاء العملية.
    pause
    exit /b
)

git branch -M main
git remote remove origin 2>nul
git remote add origin %REPO_URL%
echo.
echo جاري رفع الملفات إلى GitHub...
git push -u origin main

echo.
echo ======================================================================
echo تم الرفع بنجاح! الآن توجه إلى https://dashboard.render.com
echo واضغط New + -> Web Service واختر هذا المستودع.
echo ======================================================================
pause
