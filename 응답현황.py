import pandas as pd

def calculate_response_rates(csv_file_path):
    # 1. CSV 파일 읽기 (한글 깨짐을 방지하기 위해 utf-8 우선 시도 후 cp949 적용)
    try:
        df = pd.read_csv(csv_file_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(csv_file_path, encoding='cp949')
        
    # 열 이름의 앞뒤 공백 제거 (오류 방지)
    df.columns = df.columns.str.strip()
    
    # --- 만약 실제 데이터의 열 이름이 다를 경우 아래 변수를 수정해 주세요 ---
    target_name_col = '대상자'  # 대상자 이름 열
    session_col = '구분'           # 본인, 상사, 부하가 적혀있는 열 (예: 평가자 구분, 릴레이션 등)
    rate_col = '응답률'            # 응답률 열
    # -------------------------------------------------------------------------
    
    # 2. '대상자 이름'에서 '관리자' 및 '관리자숫자' (예: 관리자2) 제외하기
    # 정규표현식 '^관리자\d*$' 를 사용하여 "관리자로 시작하고 뒤에 숫자만 오거나 아무것도 없는 문자열"을 제외
    filtered_df = df[~df[target_name_col].str.contains(r'^관리자\d*$', regex=True, na=False)].copy()
    
    # 3. '응답률' 데이터 전처리 (혹시 '%' 기호가 붙어있는 문자열 처리)
    filtered_df[rate_col] = filtered_df[rate_col].astype(str).str.replace('%', '').str.replace(',', '')
    filtered_df[rate_col] = pd.to_numeric(filtered_df[rate_col], errors='coerce')
        
    # 4. 세션별 (본인, 상사, 부하) 필터링 및 평균 도출
    target_sessions = ['본인', '상사', '부하']
    final_df = filtered_df[filtered_df[session_col].isin(target_sessions)]
    
    # 세션별 그룹화하여 평균 계산
    result = final_df.groupby(session_col)[rate_col].mean()
    
    # 결과 출력
    print("===== 대상자 범위별 평균 응답률 =====")
    for session in target_sessions:
        # 데이터에 해당 세션이 있을 때만 출력
        if session in result:
            print(f"- {session} 평균 응답률: {result[session]:.2f}%")
        else:
            print(f"- {session} 데이터가 없습니다.")
            
    return result

# ==== 코드 실행 예시 ====
csv_file_path = "C:/Users/SKTelecom/Downloads/메일_응답현황_20260623.csv"
calculate_response_rates(csv_file_path)
