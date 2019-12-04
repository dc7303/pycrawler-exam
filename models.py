class FileDiffInfo(object):
    """
    파일 변경 정보 객체

    :param file_name: 파일 이름
    :param diff_row_list: 달라진 엑셀 ROW 리스트
    """
    def __init__(self, file_name: str, diff_row_list: list):
        self.file_name = file_name
        self.diff_row_list = diff_row_list

    def get_diff_row_format_str(self):
        """
        파일 다른 정보 스트링 값으로 파싱하여 리턴
        
        :return format_str: 정리된 변경 정보 스트링
        """
        format_str = ''
        for l in self.diff_row_list:
            format_str += '>' + l + '\n'

        return format_str
