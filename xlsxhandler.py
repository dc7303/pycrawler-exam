import pandas as pd
from models import FileDiffInfo
from logger import setup_custom_logger

logger = setup_custom_logger('xlsxhandler')


def _compare_with_each_other_file_info(compare_list: list, compare_target_list) -> list:
    """
    두 파일 리스트를 비교하여 다른 파일 정보가 있다면
    해당 파일 이름을 리스트에 담아 리턴한다.

    :param compare_list: 비교할 리스트
    :param compare_target_list: 비교 대상 리스트
    :return: 다른 항목 리스트
    """
    compare_file_name_list = [v.split('/')[-1] for v in compare_list]
    target_file_name_list = [v.split('/')[-1] for v in compare_target_list]
    result_list = []
    for name in compare_file_name_list:
        if name not in target_file_name_list:
            result_list.append(name)

    return result_list


def get_dir_update_info(before_xlsx_list: list, after_xlsx_list) -> (list, list):
    """
    이전 파일 리스트와 현재 파일리스트를 비교하여
    삭제된 파일과 추가된 파일을 파악하여 반환

    :param before_xlsx_list: 이전 파일들
    :param after_xlsx_list: 업데이트 후 파일들
    :return: 삭제 파일 리스트와 생성된 파일 리스트
    """
    deleted_file_list = _compare_with_each_other_file_info(before_xlsx_list, after_xlsx_list)
    new_file_list = _compare_with_each_other_file_info(after_xlsx_list, before_xlsx_list)

    return deleted_file_list, new_file_list


def get_file_difference_info_list(current_xlsx_list: list, dir_path: str) -> list:
    """
    파일 시트 다른 부분 정보 리스트 가져오기

    :param current_xlsx_list: 현재 E-Spider 서비스명세서 엑셀 파일 리스트
    :param dir_path: 읽을 파일 디렉토리 경로

    :return list: 파일 변경된 정보 객체 리스트
    """
    diff_info_list = []
    for xlsx_ in current_xlsx_list:
        try:
            # 엑셀파일 읽기
            current_xlsx_df = pd.read_excel(xlsx_)
            file_name = xlsx_.split('/')[-1]

            # 이전 버전 조회
            old_xlsx_df = pd.read_excel(f'{dir_path}/{file_name}')

            # 시트 데이터가 같은지 비교 후 같지 않다면 상세 비교
            if not old_xlsx_df.equals(current_xlsx_df):
                logger.debug(f'Diff file ==> {file_name}')
                # 두 데이터 다른 부분 추출
                df = pd.concat([old_xlsx_df, current_xlsx_df])
                duplicates_df = df.drop_duplicates(keep=False)
                logger.debug(f'Diff row ==> {duplicates_df}')

                old_list = old_xlsx_df.values.tolist()
                cur_list = current_xlsx_df.values.tolist()

                # 변경 전 데이터, 변경 후 데이터 분류
                changed_list = []
                for r in duplicates_df.values.tolist():
                    for old in old_list[1:]:
                        if str(old) == str(r):
                            changed_list.append(f'~{old}~')

                    for cur in cur_list[1:]:
                        if str(cur) == str(r):
                            changed_list.append(f'{cur}')

                # 변경된 정보를 핸들링할 객체 생성
                logger.debug(f'chaged_list = {changed_list}')
                info = FileDiffInfo(file_name, changed_list)
                diff_info_list.append(info)

        except Exception as e:
            logger.error(e)
            continue

    return diff_info_list