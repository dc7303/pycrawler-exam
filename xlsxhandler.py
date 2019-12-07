import pandas as pd
from models import FileDiffInfo
from logger import setup_custom_logger

logger = setup_custom_logger('xlsxhandler')


def _compare_file_list(compare_list: list, compare_target_list) -> list:
    """
    두 파일 리스트를 비교하여 다른 파일 정보가 있다면
    해당 파일 이름을 리스트에 담아 리턴한다.

    :param compare_list: 비교할 리스트
    :param compare_target_list: 비교 대상 리스트
    :return: 다른 항목 리스트
    """
    result_list = []
    for name in compare_list:
        if name not in compare_target_list:
            result_list.append(name)

    return result_list


def get_dir_update_info(before_xlsx_path_list: list, after_xlsx_path_list: list) -> (list, list):
    """
    이전 파일 리스트와 현재 파일리스트를 비교하여
    삭제된 파일과 추가된 파일을 파악하여 반환

    :param before_xlsx_path_list: 이전 파일경로 리스트
    :param after_xlsx_path_list: 업데이트 후 파일경로 리스트
    :return: 삭제 파일 리스트와 생성된 파일 리스트
    """
    after_file_name_list = [after.split('/')[-1] for after in after_xlsx_path_list]
    before_file_name_list = [before.split('/')[-1] for before in before_xlsx_path_list]
    deleted_file_list = _compare_file_list(before_file_name_list, after_file_name_list)
    new_file_list = _compare_file_list(after_file_name_list, before_file_name_list)

    return deleted_file_list, new_file_list


def get_file_diff_info_list(after_xlsx_path_list: list, before_dir_path: str) -> list:
    """
    파일 시트 다른 부분 정보 리스트 가져오기

    :param after_xlsx_path_list: 최신 서비스명세서 엑셀 파일경로 리스트
    :param before_dir_path: 읽을 파일 디렉토리 경로

    :return list: 파일 변경된 정보 객체 리스트
    """
    diff_info_list = []
    for xlsx_path in after_xlsx_path_list:
        # 엑셀파일 읽기
        try:
            after_df = pd.read_excel(xlsx_path)
            file_name = xlsx_path.split('/')[-1]

            # 이전 버전 조회
            before_df = pd.read_excel(f'{before_dir_path}/{file_name}')
        except FileNotFoundError:
            continue

        # 시트 데이터가 같은지 비교 후 같지 않다면 상세 비교
        if not before_df.equals(after_df):
            # 두 데이터 다른 부분 추출
            df = pd.concat([before_df, after_df])
            duplicates_df = df.drop_duplicates(keep=False)

            before_list = [str(r) for r in before_df.values.tolist()]
            after_list = [str(r) for r in after_df.values.tolist()]

            # 변경 전 데이터, 변경 후 데이터 분류
            changed_list = []
            duplicates_list = [str(r) for r in duplicates_df.values.tolist()]
            for row in duplicates_list:
                try:
                    before_list.index(row)
                    changed_list.append(f'~{row}~')
                except ValueError:
                    pass

                try:
                    after_list.index(row)
                    changed_list.append(row)
                except ValueError:
                    pass

            # 변경된 정보를 핸들링할 객체 생성
            info = FileDiffInfo(file_name, changed_list)
            diff_info_list.append(info)

    return diff_info_list

