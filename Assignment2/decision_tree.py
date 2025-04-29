# Environment
# OS: MacOS
# Language: Python 3.13

import sys

def main():
    args = sys.argv[1:]
    with open(args[0], 'r') as train:
        # 훈련 데이터 읽어오는 함수 추가
        train.close()
    # 훈련 수행 코드 구현
    with open(args[1], 'r') as test:
        # 테스트 데이터 읽어오는 함수 추가
        test.close()
    # 테스트 수행 코드 구현
    with open(args[2], 'w') as result:
        # 결과 작성하는 함수 추가
        result.close()

if __name__ == '__main__':
    main()
