from slacker import Slacker


class Slack(object):
    """
    슬랙 API 핸들링을 위한 객체

    :param token: 슬랙 API 토큰
    :param channel: 채널 이름
    :param username: 전송자 이름
    """
    def __init__(self, token: str, channel: str, username: str):
        self.slack = Slacker(token)
        self.channel = channel
        self.username = username

    def send_slack_msg(self, text: str = '변경된 내용이 없습니다.'):
        """
        슬랙 메세지 전송

        :param text: 변경 내용
        """
        self.slack.chat.post_message(
            channel=self.channel,
            username=self.username,
            text=text)


def gen_total_file_update_info_text(deleted_file_list: list, new_file_list: list):
    """
    전체파일 업데이트 정보 텍스트 생성.
    추가/삭제 된 내용을 텍스트로 가져온다.

    :param deleted_file_list: 삭제된 파일리스트
    :param new_file_list: 추가된 파일리스트
    """
    text = '*전체 서비스 명세서 추가/삭제 업데이트 리스트*: \n\n'

    if len(deleted_file_list) != 0:
        for f in deleted_file_list:
            text += f'>삭제 - {f}'
        text += '\n'

    if len(new_file_list) != 0:
        for f in new_file_list:
            text += f'>추가 - {f}'
        text += '\n'

    if len(deleted_file_list) == 0 and len(new_file_list) == 0:
        text += '>추가/삭제 된 파일이 없습니다.'

    return text


def gen_diff_row_info_text(file_diff_info_list: list):
    """
    파일별 ROW에 대한 변경 정보를 텍스트로 생성한다.

    :param file_diff_info_list: 파일 ROW 다른 정보 리스트
    """
    text = '*명세서별 변경된 ROW 정보*: \n\n'

    if len(file_diff_info_list) != 0:
        for f in file_diff_info_list:
            text += f'`{f.file_name}`:\n{f.get_diff_row_format_str()}\n'
    else:
        text += '>변경된 정보가 없습니다.'

    return text
            


