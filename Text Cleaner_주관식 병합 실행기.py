import pandas as pd  # type: ignore
import os

def merge_subjective_responses(file_path):
    print(f"[{file_path}] 처리를 시작합니다...")
    
    try:
        # 데이터 불러오기
        df = pd.read_excel(file_path)
        print(f"총 {len(df)}행의 데이터를 불러왔습니다.")
        
        # A열(첫 번째 열)의 이름 확인
        id_col = df.columns[0]
        print(f"기준 ID 컬럼명: '{id_col}'\n")
        
        # --- 외국어 응답 번역 추가 ---
        if 'LANG' in df.columns:
            print("LANG 컬럼이 감지되었습니다. '영문' 또는 '중문' 응답을 한글로 번역 중입니다. 잠시만 기다려주세요...")
            try:
                from deep_translator import GoogleTranslator  # type: ignore
                translator = GoogleTranslator(source='auto', target='ko')
                
                translate_mask = df['LANG'].isin(['영문', '중문'])
                cols_to_translate = [c for c in df.columns if c not in [id_col, 'LANG']]
                
                translated_count: int = 0
                for index, row in df[translate_mask].iterrows():
                    for col in cols_to_translate:
                        val = row[col]  # type: ignore
                        if pd.notna(val) and str(val).strip() != '':
                            try:
                                translated_text = translator.translate(str(val))
                                df.at[index, col] = translated_text
                                translated_count += 1  # type: ignore
                            except Exception:
                                pass
                                
                if translated_count > 0:
                    print(f"총 {translated_count}개의 응답이 한글로 번역되었습니다.\n")
                else:
                    print("번역할 대상이 없었거나 모두 완료되었습니다.\n")
            except ImportError:
                print("⚠️ deep-translator 라이브러리가 설치되지 않아 번역을 건너뜁니다.")
                print("명령 프롬프트에서 'pip install deep-translator'를 실행해주세요.\n")
        # -----------------------------
        
        # 텍스트 병합 함수 (빈칸 제외, 줄바꿈으로 연결)
        def merge_texts(x):
            try:
                # 결측치(NaN) 제외 및 문자열 변환 (공백만 있는 응답 제외)
                valid_texts = [str(text) for text in x.dropna() if str(text).strip() != '']
                return '\n'.join(valid_texts)
            except Exception:
                return ''
                
        # A열 기준으로 모든 컬럼 병합
        print("데이터 병합 중 (시간이 조금 걸릴 수 있습니다)...")
        # groupby 후에 각 컬럼별로 merge_texts 함수 적용
        grouped_df = df.groupby(id_col, as_index=False).agg(merge_texts)
        
        print(f"병합 완료! 총 {len(grouped_df)}개의 고유 ID가 있습니다.")
        
        # 기존 파일에 새 시트 추가
        # openpyxl을 엔진으로 사용하여 원본을 보존하면서 시트 추가
        print("엑셀 파일에 '병합결과' 시트를 추가하여 저장합니다...")
        
        # 만약 이미 병합결과 시트가 있다면 덮어쓰거나 처리하는 로직을 방지하기 위해 
        # 새로운 시트 이름을 생성할 수도 있지만 여기서는 기본적으로 실행합니다.
        with pd.ExcelWriter(file_path, mode='a', engine='openpyxl') as writer:
            grouped_df.to_excel(writer, sheet_name='병합결과', index=False)
            
        print(f"✅ 처리가 완료되었습니다. '{file_path}' 파일을 열어 '병합결과' 시트를 확인해보세요!")
        
    except PermissionError:
        print(f"❌ 오류: '{file_path}' 파일이 이미 엑셀에서 열려있습니다.")
        print("열려있는 엑셀 파일을 완전히 닫은 후 다시 실행해주세요.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("        주관식 응답 데이터 ID별 병합기")
    print("=" * 50)
    
    excel_file = input("처리할 엑셀 파일의 이름(또는 경로)을 입력하세요 (예: data.xlsx) : ")
    
    # 입력받은 파일명 좌우 공백이나 따옴표 제거 (경로 복사 시 발생하는 따옴표 방지)
    excel_file = excel_file.strip().strip('"').strip("'")
    
    if os.path.exists(excel_file):
        merge_subjective_responses(excel_file)
    else:
        print(f"\n❌ 파일을 찾을 수 없습니다: '{excel_file}'")
        print("현재 스크립트가 있는 폴더에 엑셀 파일이 있는지, 파일명과 확장자(.xlsx)가 정확한지 확인해주세요.")
    
    input("\n종료하려면 엔터 키를 누르세요...")
