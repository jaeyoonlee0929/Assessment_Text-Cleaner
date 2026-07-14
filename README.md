# Text Cleaner Ver3.1

Google Sheets의 텍스트를 OpenAI API로 정리하고 결과를 다시 시트에 기록하는 Jupyter Notebook입니다.

## 1. 설치

PowerShell에서 다음 명령을 실행합니다.

```powershell
git clone <REPOSITORY_URL>
cd Text-Cleaner-Ver3-1-GitHub
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

## 2. 비밀정보 설정

복사한 `.env` 파일을 열어 다음 값을 실제 값으로 변경합니다.

```dotenv
OPENAI_API_KEY=your_openai_api_key
GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\your\service-account.json
SPREADSHEET_URL=https://docs.google.com/spreadsheets/d/your_sheet_id/edit
```

- `.env`와 Google 서비스 계정 JSON은 로컬에만 보관합니다.
- 서비스 계정 이메일에 대상 Google Sheet 접근 권한을 부여해야 합니다.
- 기존 노트북에 기록했던 키는 폐기하고 새 키를 사용하세요.

## 3. 실행

가상환경을 활성화한 뒤 Jupyter에서 `Text Cleaner_Ver3_1.ipynb`를 열고 코드 셀을 실행합니다.

```powershell
jupyter notebook
```

Jupyter가 설치되어 있지 않으면 다음 명령으로 설치할 수 있습니다.

```powershell
pip install jupyter
```

실행 결과 CSV는 `backup_results/`에 생성되며 Git에 포함되지 않습니다.

## GitHub에 포함되는 파일

- `Text Cleaner_Ver3_1.ipynb`
- `.env.example`
- `.gitignore`
- `requirements.txt`
- `README.md`

실제 `.env`, Google 인증 JSON, 결과 CSV 및 원본 진단 데이터는 업로드하지 마세요.
