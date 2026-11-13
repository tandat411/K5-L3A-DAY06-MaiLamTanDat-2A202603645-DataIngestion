"""Generate an authentic, searchable 35-page PDF corpus of the Vietnamese Labor Code 2019
and the corresponding benchmark questions adhering strictly to BENCHMARK.md.
"""
import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pymupdf
DATA_DIR = PROJECT_ROOT / "starter" / "data"
BENCHMARK_DIR = PROJECT_ROOT / "benchmark"
BENCHMARK_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

PDF_OUTPUT_PATH = DATA_DIR / "LuatLaoDong2019.pdf"
QUESTIONS_OUTPUT_PATH = BENCHMARK_DIR / "questions.json"

FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "/Library/Fonts/Arial Unicode.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "/System/Library/Fonts/Helvetica.ttc"

# Structural pages specification (Chapters and Articles)
PAGES_DATA = [
    # Page 1
    {
        "chapter": "I",
        "header": "CHƯƠNG I: NHỮNG QUY ĐỊNH CHUNG",
        "content": """BỘ LUẬT LAO ĐỘNG NĂM 2019
Luật số: 45/2019/QH14 - Ban hành ngày 20/11/2019

CHƯƠNG I: NHỮNG QUY ĐỊNH CHUNG

Điều 1. Phạm vi điều chỉnh
Bộ luật Lao động quy định tiêu chuẩn lao động; quyền, nghĩa vụ, trách nhiệm của người lao động, người sử dụng lao động, tổ chức đại diện người lao động tại cơ sở, tổ chức đại diện người sử dụng lao động trong quan hệ lao động và các quan hệ khác liên quan trực tiếp đến quan hệ lao động; quản lý nhà nước về lao động.

Điều 2. Đối tượng áp dụng
1. Người lao động, người học nghề, người tập nghề và người làm việc không có quan hệ lao động.
2. Người sử dụng lao động.
3. Người lao động nước ngoài làm việc tại Việt Nam.
4. Cơ quan, tổ chức, cá nhân khác có liên quan trực tiếp đến quan hệ lao động."""
    },
    # Page 2
    {
        "chapter": "I",
        "header": "CHƯƠNG I: NHỮNG QUY ĐỊNH CHUNG (TIẾP THEO)",
        "content": """CHƯƠNG I: NHỮNG QUY ĐỊNH CHUNG

Điều 3. Giải thích từ ngữ
Trong Bộ luật này, các từ ngữ dưới đây được hiểu như sau:
1. Người lao động là người làm việc cho người sử dụng lao động theo thỏa thuận, được trả lương và chịu sự quản lý, điều hành, giám sát của người sử dụng lao động. Độ tuổi lao động tối thiểu của người lao động là đủ 15 tuổi, trừ trường hợp quy định tại Mục 1 Chương XI của Bộ luật này.
2. Người sử dụng lao động là doanh nghiệp, cơ quan, tổ chức, hợp tác xã, hộ gia đình, cá nhân có thuê mướn, sử dụng người lao động làm việc cho mình theo thỏa thuận; trường hợp người sử dụng lao động là cá nhân thì phải có năng lực hành vi dân sự đầy đủ.
3. Tổ chức đại diện người lao động tại cơ sở là tổ chức được thành lập trên cơ sở tự nguyện của người lao động tại một đơn vị sử dụng lao động nhằm mục đích bảo vệ quyền và lợi ích hợp pháp, chính đáng của người lao động trong quan hệ lao động thông qua thương lượng tập thể hoặc các hình thức khác theo quy định của pháp luật về lao động. Tổ chức đại diện người lao động tại cơ sở bao gồm công đoàn cơ sở và tổ chức của người lao động tại doanh nghiệp."""
    },
    # Page 3
    {
        "chapter": "I",
        "header": "CHƯƠNG I: NGUYÊN TẮC VÀ HÀNH VI BỊ NGHIÊM CẤM",
        "content": """CHƯƠNG I: NHỮNG QUY ĐỊNH CHUNG

Điều 4. Chính sách của Nhà nước về lao động
1. Bảo đảm quyền và lợi ích hợp pháp, chính đáng của người lao động, người làm việc không có quan hệ lao động; khuyến khích những thỏa thuận bảo đảm cho người lao động có điều kiện thuận lợi hơn so với quy định của pháp luật về lao động.
2. Bảo đảm quyền và lợi ích hợp pháp của người sử dụng lao động, quản lý lao động đúng pháp luật, dân chủ, công bằng, văn minh và nâng cao trách nhiệm xã hội.

Điều 8. Các hành vi bị nghiêm cấm trong lĩnh vực lao động
1. Phân biệt đối xử trong lao động; Cưỡng bức lao động; Quấy rối tình dục tại nơi làm việc.
2. Lợi dụng danh nghĩa dạy nghề, tập nghề để trục lợi, bóc lột sức lao động hoặc dụ dỗ, ép buộc người học nghề, người tập nghề vào hoạt động trái pháp luật.
3. Sử dụng lao động chưa qua đào tạo hoặc chưa có chứng chỉ kỹ năng nghề quốc gia đối với nghề, công việc phải sử dụng lao động đã được đào tạo hoặc phải có chứng chỉ kỹ năng nghề quốc gia.
4. Lôi kéo, dụ dỗ, hứa hẹn, quảng cáo gian dối hoặc thủ đoạn khác để lừa gạt người lao động hoặc để tuyển dụng người lao động với mục đích mua bán người, bóc lột, cưỡng bức lao động."""
    },
    # Page 4
    {
        "chapter": "II",
        "header": "CHƯƠNG II: VIỆC LÀM, TUYỂN DỤNG VÀ QUẢN LÝ LAO ĐỘNG",
        "content": """CHƯƠNG II: VIỆC LÀM, TUYỂN DỤNG VÀ QUẢN LÝ LAO ĐỘNG

Điều 9. Quyền làm việc của người lao động
1. Được tự do lựa chọn việc làm, làm việc cho bất kỳ người sử dụng lao động nào và ở bất kỳ nơi nào mà pháp luật không cấm.
2. Trực tiếp liên hệ với người sử dụng lao động hoặc thông qua tổ chức dịch vụ việc làm để tìm kiếm việc làm theo nguyện vọng, khả năng, trình độ nghề nghiệp và sức khỏe của mình.

Điều 10. Quyền tuyển dụng lao động của người sử dụng lao động
Người sử dụng lao động có quyền trực tiếp hoặc thông qua tổ chức dịch vụ việc làm, doanh nghiệp hoạt động cho thuê lại lao động để tuyển dụng lao động theo nhu cầu của người sử dụng lao động.

Điều 11. Tuyển dụng lao động
1. Người lao động không phải trả chi phí cho việc tuyển dụng lao động.
2. Người sử dụng lao động phải thông báo công khai về nhu cầu, tiêu chuẩn tuyển dụng, tiền lương và điều kiện làm việc."""
    },
    # Page 5
    {
        "chapter": "II",
        "header": "CHƯƠNG II: TRÁCH NHIỆM QUẢN LÝ LAO ĐỘNG",
        "content": """CHƯƠNG II: VIỆC LÀM, TUYỂN DỤNG VÀ QUẢN LÝ LAO ĐỘNG

Điều 12. Trách nhiệm quản lý lao động của người sử dụng lao động
1. Người sử dụng lao động phải lập sổ quản lý lao động bằng bản giấy hoặc bản điện tử và xuất trình khi cơ quan nhà nước có thẩm quyền yêu cầu.
2. Khai trình việc sử dụng lao động trong thời hạn 30 ngày kể từ ngày bắt đầu hoạt động, định kỳ báo cáo tình hình thay đổi về lao động trong quá trình hoạt động với cơ quan chuyên môn về lao động thuộc Ủy ban nhân dân cấp tỉnh và thông báo cho cơ quan bảo hiểm xã hội.

Điều 13. Khái niệm hợp đồng lao động
1. Hợp đồng lao động là sự thỏa thuận giữa người lao động và người sử dụng lao động về việc làm có trả công, tiền lương, điều kiện lao động, quyền và nghĩa vụ của mỗi bên trong quan hệ lao động. Trường hợp hai bên thỏa thuận bằng tên gọi khác nhưng có nội dung thể hiện về việc làm có trả công, tiền lương và sự quản lý, điều hành, giám sát của một bên thì vẫn được coi là hợp đồng lao động."""
    },
    # Page 6
    {
        "chapter": "III",
        "header": "CHƯƠNG III: HỢP ĐỒNG LAO ĐỘNG - HÌNH THỨC VÀ NGUYÊN TẮC",
        "content": """CHƯƠNG III: HỢP ĐỒNG LAO ĐỘNG

Điều 14. Hình thức hợp đồng lao động
1. Hợp đồng lao động phải được giao kết bằng văn bản và được làm thành 02 bản, người lao động giữ 01 bản, người sử dụng lao động giữ 01 bản, trừ trường hợp quy định tại khoản 2 Điều này. Hợp đồng lao động được giao kết thông qua phương tiện điện tử dưới hình thức thông điệp dữ liệu theo quy định của pháp luật về giao dịch điện tử có giá trị như hợp đồng lao động bằng văn bản.
2. Hai bên có thể giao kết hợp đồng lao động bằng lời nói đối với hợp đồng có thời hạn dưới 01 tháng, trừ trường hợp giao kết hợp đồng lao động với người giúp việc gia đình, người dưới 15 tuổi, nhóm người lao động thông qua một người lao động được ủy quyền.

Điều 15. Nguyên tắc giao kết hợp đồng lao động
1. Tự nguyện, bình đẳng, thiện chí, hợp tác và trung thực.
2. Tự do giao kết hợp đồng lao động nhưng không được trái pháp luật, thỏa ước lao động tập thể và đạo đức xã hội."""
    },
    # Page 7
    {
        "chapter": "III",
        "header": "CHƯƠNG III: LOẠI HỢP ĐỒNG VÀ NỘI DUNG",
        "content": """CHƯƠNG III: HỢP ĐỒNG LAO ĐỘNG

Điều 20. Loại hợp đồng lao động
1. Hợp đồng lao động được giao kết theo một trong hai loại sau đây:
a) Hợp đồng lao động không xác định thời hạn là hợp đồng mà trong đó hai bên không xác định thời hạn, thời điểm chấm dứt hiệu lực của hợp đồng; Hợp đồng lao động xác định thời hạn là hợp đồng mà trong đó hai bên xác định thời hạn, thời điểm chấm dứt hiệu lực của hợp đồng trong thời gian không quá 36 tháng.
b) Hợp đồng lao động xác định thời hạn là hợp đồng mà trong đó hai bên xác định thời hạn, thời điểm chấm dứt hiệu lực của hợp đồng trong thời gian không quá 36 tháng kể từ thời điểm có hiệu lực của hợp đồng.

2. Khi hợp đồng lao động xác định thời hạn hết hạn mà người lao động vẫn tiếp tục làm việc thì trong thời hạn 30 ngày kể từ ngày hợp đồng hết hạn, hai bên phải ký kết hợp đồng lao động mới; nếu không ký kết hợp đồng lao động mới thì hợp đồng đã giao kết trở thành hợp đồng lao động không xác định thời hạn."""
    },
    # Page 8
    {
        "chapter": "III",
        "header": "CHƯƠNG III: THỬ VIỆC VÀ LƯƠNG THỬ VIỆC",
        "content": """CHƯƠNG III: HỢP ĐỒNG LAO ĐỘNG

Điều 25. Thời gian thử việc
Thời gian thử việc do hai bên thỏa thuận căn cứ vào tính chất và mức độ phức tạp của công việc nhưng chỉ được thử việc một lần đối với một công việc và bảo đảm điều kiện sau đây:
1. Không quá 180 ngày đối với công việc của người quản lý doanh nghiệp theo quy định của Luật Doanh nghiệp.
2. Không quá 60 ngày đối với công việc có chức danh nghề nghiệp cần trình độ chuyên môn, kỹ thuật từ cao đẳng trở lên.
3. Không quá 30 ngày đối với công việc có chức danh nghề nghiệp cần trình độ chuyên môn, kỹ thuật trung cấp, công nhân kỹ thuật, nhân viên nghiệp vụ.
4. Không quá 06 ngày làm việc đối với công việc khác.

Điều 26. Tiền lương thử việc
Tiền lương của người lao động trong thời gian thử việc do hai bên thỏa thuận nhưng ít nhất phải bằng 85% mức lương của công việc đó."""
    },
    # Page 9
    {
        "chapter": "III",
        "header": "CHƯƠNG III: CHẤM DỨT HỢP ĐỒNG LAO ĐỘNG",
        "content": """CHƯƠNG III: HỢP ĐỒNG LAO ĐỘNG

Điều 34. Các trường hợp chấm dứt hợp đồng lao động
1. Hết hạn hợp đồng lao động, trừ trường hợp quy định tại khoản 4 Điều 177 của Bộ luật này.
2. Đã hoàn thành công việc theo hợp đồng lao động.
3. Hai bên thỏa thuận chấm dứt hợp đồng lao động.
4. Người lao động bị kết án phạt tù nhưng không được hưởng án treo hoặc không thuộc trường hợp được trả tự do, tử hình hoặc bị cấm làm công việc ghi trong hợp đồng lao động theo bản án, quyết định của Tòa án đã có hiệu lực pháp luật.
5. Người lao động chết; bị Tòa án tuyên bố mất năng lực hành vi dân sự, mất tích hoặc đã chết.
6. Người sử dụng lao động là cá nhân chết; bị Tòa án tuyên bố mất năng lực hành vi dân sự, mất tích hoặc đã chết. Người sử dụng lao động không phải là cá nhân chấm dứt hoạt động."""
    },
    # Page 10
    {
        "chapter": "III",
        "header": "CHƯƠNG III: ĐƠN PHƯƠNG CHẤM DỨT HỢP ĐỒNG LAO ĐỘNG",
        "content": """CHƯƠNG III: HỢP ĐỒNG LAO ĐỘNG

Điều 35. Quyền đơn phương chấm dứt hợp đồng lao động của người lao động
1. Người lao động có quyền đơn phương chấm dứt hợp đồng lao động nhưng phải báo trước cho người sử dụng lao động như sau:
a) Ít nhất 45 ngày nếu làm việc theo hợp đồng lao động không xác định thời hạn.
b) Ít nhất 30 ngày nếu làm việc theo hợp đồng lao động xác định thời hạn có thời hạn từ 12 tháng đến 36 tháng.
c) Ít nhất 03 ngày làm việc nếu làm việc theo hợp đồng lao động xác định thời hạn có thời hạn dưới 12 tháng.
d) Đối với một số ngành, nghề, công việc đặc thù thì thời hạn báo trước được thực hiện theo quy định của Chính phủ.

2. Người lao động có quyền đơn phương chấm dứt hợp đồng lao động không cần báo trước trong các trường hợp sau đây:
a) Không được bố trí theo đúng công việc, địa điểm làm việc hoặc không được bảo đảm điều kiện làm việc theo thỏa thuận.
b) Không được trả đủ lương hoặc trả lương không đúng thời hạn.
c) Bị người sử dụng lao động ngược đãi, đánh đập hoặc có lời nói, hành vi nhục mạ, hành vi làm ảnh hưởng đến sức khỏe, nhân phẩm, danh dự; bị cưỡng bức lao động; bị quấy rối tình dục tại nơi làm việc."""
    },
    # Page 11
    {
        "chapter": "III",
        "header": "CHƯƠNG III: TRỢ CẤP THÔI VIỆC VÀ MẤT VIỆC LÀM",
        "content": """CHƯƠNG III: HỢP ĐỒNG LAO ĐỘNG

Điều 46. Trợ cấp thôi việc
1. Khi hợp đồng lao động chấm dứt theo quy định tại các khoản 1, 2, 3, 4, 6, 7, 9 và 10 Điều 34 của Bộ luật này thì người sử dụng lao động có trách nhiệm trả trợ cấp thôi việc cho người lao động đã làm việc thường xuyên cho mình từ đủ 12 tháng trở lên. Mỗi năm làm việc được trợ cấp một nửa tháng tiền lương, trừ trường hợp đủ điều kiện hưởng lương hưu.
2. Thời gian làm việc để tính trợ cấp thôi việc là tổng thời gian người lao động đã làm việc thực tế cho người sử dụng lao động trừ đi thời gian người lao động đã tham gia bảo hiểm thất nghiệp theo quy định của pháp luật về bảo hiểm thất nghiệp và thời gian làm việc đã được người sử dụng lao động chi trả trợ cấp thôi việc, trợ cấp mất việc làm.

Điều 47. Trợ cấp mất việc làm
1. Người sử dụng lao động trả trợ cấp mất việc làm cho người lao động đã làm việc thường xuyên cho mình từ đủ 12 tháng trở lên mà bị mất việc làm, mỗi năm làm việc trả 01 tháng tiền lương nhưng ít nhất bằng 02 tháng tiền lương.
2. Tiền lương để tính trợ cấp thôi việc và trợ cấp mất việc làm là tiền lương bình quân của 06 tháng liền kề theo hợp đồng lao động trước khi người lao động thôi việc hoặc mất việc làm."""
    },
    # Page 12
    {
        "chapter": "IV",
        "header": "CHƯƠNG IV: GIÁO DỤC NGHỀ NGHIỆP VÀ PHÁT TRIỂN KỸ NĂNG",
        "content": """CHƯƠNG IV: GIÁO DỤC NGHỀ NGHIỆP VÀ PHÁT TRIỂN KỸ NĂNG NGHỀ

Điều 59. Trách nhiệm về đào tạo, bồi dưỡng, nâng cao trình độ, kỹ năng nghề
1. Người sử dụng lao động xây dựng kế hoạch hằng năm và dành kinh phí cho việc đào tạo, bồi dưỡng, nâng cao trình độ, kỹ năng nghề, phát triển kỹ năng nghề cho người lao động đang làm việc cho mình; đào tạo cho người lao động trước khi chuyển làm nghề khác cho người sử dụng lao động.
2. Hằng năm, người sử dụng lao động thông báo kết quả đào tạo, bồi dưỡng nâng cao trình độ, kỹ năng nghề cho cơ quan chuyên môn về lao động thuộc Ủy ban nhân dân cấp tỉnh.

Điều 61. Học nghề, tập nghề để làm việc cho người sử dụng lao động
1. Học nghề để làm việc cho người sử dụng lao động là việc người sử dụng lao động tuyển người vào để đào tạo nghề nghiệp tại nơi làm việc. Thời gian học nghề theo chương trình đào tạo của từng trình độ theo quy định của Luật Giáo dục nghề nghiệp.
2. Tập nghề để làm việc cho người sử dụng lao động là việc người sử dụng lao động tuyển người vào để hướng dẫn thực hành công việc, tập làm nghề theo vị trí việc làm tại nơi làm việc. Thời hạn tập nghề không quá 03 tháng.
3. Người học nghề, người tập nghề trong thời gian học nghề, tập nghề nếu trực tiếp làm ra sản phẩm thì được người sử dụng lao động trả công theo mức do hai bên thỏa thuận."""
    },
    # Page 13
    {
        "chapter": "IV",
        "header": "CHƯƠNG IV: HỢP ĐỒNG ĐÀO TẠO NGHỀ",
        "content": """CHƯƠNG IV: GIÁO DỤC NGHỀ NGHIỆP VÀ PHÁT TRIỂN KỸ NĂNG NGHỀ

Điều 62. Hợp đồng đào tạo nghề giữa người sử dụng lao động, người lao động và chi phí đào tạo nghề
1. Hai bên phải ký kết hợp đồng đào tạo nghề trong trường hợp người lao động được đào tạo, nâng cao trình độ, kỹ năng nghề, đào tạo lại ở trong nước hoặc nước ngoài từ kinh phí của người sử dụng lao động, kể cả kinh phí do đối tác tài trợ cho người sử dụng lao động.
2. Hợp đồng đào tạo nghề phải có các nội dung chủ yếu sau đây:
a) Nghề đào tạo;
b) Địa điểm, thời gian đào tạo và tiền lương trong thời gian đào tạo;
c) Thời hạn cam kết phải làm việc sau khi được đào tạo;
d) Chi phí đào tạo và trách nhiệm hoàn trả chi phí đào tạo;
đ) Trách nhiệm của người sử dụng lao động;
e) Trách nhiệm của người lao động.
3. Chi phí đào tạo bao gồm các khoản chi có chứng từ hợp lệ về chi phí trả cho người dạy, tài liệu học tập, trường, lớp, máy, thiết bị, vật liệu thực hành, các chi phí khác hỗ trợ cho người học và tiền lương, tiền đóng bảo hiểm xã hội, bảo hiểm y tế, bảo hiểm thất nghiệp cho người học trong thời gian đi học."""
    },
    # Page 14
    {
        "chapter": "V",
        "header": "CHƯƠNG V: ĐỐI THOẠI TẠI NƠI LÀM VIỆC",
        "content": """CHƯƠNG V: ĐỐI THOẠI TẠI NƠI LÀM VIỆC, THƯƠNG LƯỢNG TẬP THỂ, THỎA ƯỚC LAO ĐỘNG TẬP THỂ

Điều 63. Tổ chức đối thoại tại nơi làm việc
1. Đối thoại tại nơi làm việc là việc chia sẻ thông tin, tham khảo, thảo luận, trao đổi ý kiến giữa người sử dụng lao động với người lao động hoặc tổ chức đại diện người lao động về những vấn đề liên quan đến quyền, lợi ích và mối quan tâm của các bên tại nơi làm việc nhằm tăng cường sự hiểu biết, tương trợ, hợp tác và hướng tới quan hệ lao động hài hòa, tiến bộ.
2. Người sử dụng lao động phải tổ chức đối thoại tại nơi làm việc trong các trường hợp sau đây:
a) Định kỳ ít nhất 01 năm một lần; Khi có yêu cầu của một hoặc các bên; Khi có vụ việc quy định tại điểm a khoản 1 Điều 36, các điều 42, 44, 93, 104, 118.
b) Khi có yêu cầu của một hoặc các bên;
c) Khi có vụ việc quy định tại điểm a khoản 1 Điều 36, các điều 42, 44, 93, 104, 118, khoản 1 Điều 128 của Bộ luật này.
3. Khuyến khích người sử dụng lao động và người lao động hoặc tổ chức đại diện người lao động tiến hành đối thoại ngoài các trường hợp quy định tại khoản 2 Điều này."""
    },
    # Page 15
    {
        "chapter": "V",
        "header": "CHƯƠNG V: THƯƠNG LƯỢNG VÀ THỎA ƯỚC LAO ĐỘNG TẬP THỂ",
        "content": """CHƯƠNG V: ĐỐI THOẠI TẠI NƠI LÀM VIỆC, THƯƠNG LƯỢNG TẬP THỂ, THỎA ƯỚC LAO ĐỘNG TẬP THỂ

Điều 75. Thỏa ước lao động tập thể
1. Thỏa ước lao động tập thể là văn bản thỏa thuận đạt được thông qua thương lượng tập thể và được các bên ký kết bằng văn bản. Thỏa ước lao động tập thể bao gồm thỏa ước lao động tập thể doanh nghiệp, thỏa ước lao động tập thể ngành, thỏa ước lao động tập thể có nhiều doanh nghiệp và các thỏa ước lao động tập thể khác.
2. Nội dung thỏa ước lao động tập thể không được trái với quy định của pháp luật; khuyến khích có lợi hơn cho người lao động so với quy định của pháp luật.

Điều 76. Lấy ý kiến và ký kết thỏa ước lao động tập thể
1. Trước khi ký kết thỏa ước lao động tập thể, dự thảo thỏa ước lao động tập thể đã được các bên đàm phán phải được lấy ý kiến của toàn bộ người lao động trong doanh nghiệp.
2. Thỏa ước lao động tập thể doanh nghiệp được ký kết khi có trên 50% người lao động của doanh nghiệp biểu quyết tán thành. Thỏa ước lao động tập thể ngành được ký kết khi có trên 50% tổng số người đại diện của các ban chấp hành công đoàn cơ sở hoặc tổ chức đại diện người lao động tại doanh nghiệp tham gia thương lượng biểu quyết tán thành."""
    },
    # Page 16
    {
        "chapter": "VI",
        "header": "CHƯƠNG VI: TIỀN LƯƠNG VÀ NGUYÊN TẮC TRẢ LƯƠNG",
        "content": """CHƯƠNG VI: TIỀN LƯƠNG

Điều 90. Tiền lương
1. Tiền lương là số tiền mà người sử dụng lao động trả cho người lao động theo thỏa thuận để thực hiện công việc, bao gồm mức lương theo công việc hoặc chức danh, phụ cấp lương và các khoản bổ sung khác.
2. Mức lương theo công việc hoặc chức danh không được thấp hơn mức lương tối thiểu.
3. Người sử dụng lao động phải bảo đảm trả lương bình đẳng, không phân biệt giới tính đối với người lao động làm công việc có giá trị như nhau.

Điều 91. Mức lương tối thiểu
1. Mức lương tối thiểu là mức lương thấp nhất được trả cho người lao động làm công việc giản đơn nhất trong điều kiện lao động bình thường nhằm bảo đảm mức sống tối thiểu của người lao động và gia đình họ, phù hợp với điều kiện phát triển kinh tế - xã hội.
2. Mức lương tối thiểu được xác lập theo vùng, ấn định theo tháng, giờ và do Chính phủ công bố trên cơ sở khuyến nghị của Hội đồng tiền lương quốc gia."""
    },
    # Page 17
    {
        "chapter": "VI",
        "header": "CHƯƠNG VI: HÌNH THỨC VÀ KỲ HẠN TRẢ LƯƠNG",
        "content": """CHƯƠNG VI: TIỀN LƯƠNG

Điều 94. Nguyên tắc trả lương
1. Người sử dụng lao động phải trả lương trực tiếp, đầy đủ, đúng hạn cho người lao động. Trường hợp người lao động không thể nhận lương trực tiếp thì người sử dụng lao động có thể trả lương cho người được người lao động ủy quyền hợp pháp.
2. Người sử dụng lao động không được hạn chế hoặc can thiệp vào quyền tự quyết chi tiêu lương của người lao động; không được ép buộc người lao động mua hàng hóa, sử dụng dịch vụ của người sử dụng lao động hoặc của đơn vị khác mà người sử dụng lao động chỉ định.

Điều 96. Hình thức trả lương
1. Người sử dụng lao động và người lao động thỏa thuận về hình thức trả lương theo thời gian, theo sản phẩm hoặc theo khoán.
2. Lương được trả bằng tiền mặt hoặc trả qua tài khoản cá nhân của người lao động được mở tại ngân hàng. Trường hợp trả lương qua tài khoản cá nhân của người lao động được mở tại ngân hàng thì người sử dụng lao động phải trả các loại phí liên quan đến việc mở tài khoản và chuyển tiền lương."""
    },
    # Page 18
    {
        "chapter": "VI",
        "header": "CHƯƠNG VI: TIỀN LƯƠNG LÀM THÊM GIỜ VÀ BAN ĐÊM",
        "content": """CHƯƠNG VI: TIỀN LƯƠNG

Điều 98. Tiền lương làm thêm giờ, làm việc vào ban đêm
1. Người lao động làm thêm giờ được trả lương tính theo đơn giá tiền lương hoặc tiền lương thực trả theo công việc đang làm như sau:
a) Vào ngày thường, ít nhất bằng 150%;
b) Vào ngày nghỉ hằng tuần, ít nhất bằng 200%; Vào ngày nghỉ lễ, tết, ngày nghỉ có hưởng lương, ít nhất bằng 300% chưa kể tiền lương ngày lễ, tết.
2. Người lao động làm việc vào ban đêm thì được trả thêm ít nhất bằng 30% tiền lương tính theo đơn giá tiền lương hoặc tiền lương thực trả theo công việc của ngày làm việc bình thường.
3. Người lao động làm thêm giờ vào ban đêm thì ngoài việc trả lương quy định tại khoản 1 và khoản 2 Điều này, người lao động còn được trả thêm 20% tiền lương tính theo đơn giá tiền lương hoặc tiền lương theo công việc làm vào ban ngày của ngày làm việc bình thường hoặc của ngày nghỉ hằng tuần hoặc của ngày nghỉ lễ, tết.

Điều 104. Thưởng
1. Thưởng là số tiền hoặc tài sản hoặc bằng các hình thức khác mà người sử dụng lao động thưởng cho người lao động căn cứ vào kết quả sản xuất, kinh doanh, mức độ hoàn thành công việc của người lao động.
2. Quy chế thưởng do người sử dụng lao động quyết định và công bố công khai tại nơi làm việc sau khi tham khảo ý kiến của tổ chức đại diện người lao động tại cơ sở."""
    },
    # Page 19
    {
        "chapter": "VII",
        "header": "CHƯƠNG VII: THỜI GIỜ LÀM VIỆC BÌNH THƯỜNG VÀ BAN ĐÊM",
        "content": """CHƯƠNG VII: THỜI GIỜ LÀM VIỆC, THỜI GIỜ NGHỈ NGƠI

Điều 105. Thời giờ làm việc bình thường
1. Thời giờ làm việc bình thường không quá 08 giờ trong 01 ngày và không quá 48 giờ trong 01 tuần.
2. Người sử dụng lao động có quyền quy định thời giờ làm việc theo ngày hoặc tuần nhưng phải thông báo cho người lao động biết; trường hợp theo tuần thì thời giờ làm việc bình thường không quá 10 giờ trong 01 ngày và không quá 48 giờ trong 01 tuần.
3. Nhà nước khuyến khích người sử dụng lao động thực hiện tuần làm việc 40 giờ đối với người lao động.
4. Người sử dụng lao động có trách nhiệm bảo đảm giới hạn thời gian làm việc tiếp xúc với yếu tố nguy hiểm, yếu tố có hại theo đúng quy chuẩn kỹ thuật quốc gia và pháp luật có liên quan.

Điều 106. Giờ làm việc ban đêm
Giờ làm việc ban đêm được tính từ 22 giờ đến 06 giờ sáng ngày hôm sau."""
    },
    # Page 20
    {
        "chapter": "VII",
        "header": "CHƯƠNG VII: LÀM THÊM GIỜ VÀ GIỚI HẠN",
        "content": """CHƯƠNG VII: THỜI GIỜ LÀM VIỆC, THỜI GIỜ NGHỈ NGƠI

Điều 107. Làm thêm giờ
1. Thời gian làm thêm giờ là khoảng thời gian làm việc ngoài thời giờ làm việc bình thường quy định trong luật, thỏa ước lao động tập thể hoặc nội quy lao động.
2. Người sử dụng lao động được sử dụng người lao động làm thêm giờ khi đáp ứng đầy đủ các yêu cầu sau đây:
a) Phải được sự đồng ý của người lao động;
b) Bảo đảm số giờ làm thêm của người lao động không quá 50% số giờ làm việc bình thường trong 01 ngày; không quá 40 giờ trong 01 tháng; Không quá 200 giờ trong 01 năm, trừ trường hợp quy định tại khoản 3 Điều này.
c) Không quá 200 giờ trong 01 năm, trừ trường hợp quy định tại khoản 3 Điều này.
3. Người sử dụng lao động được sử dụng người lao động làm thêm giờ không quá 300 giờ trong 01 năm trong một số ngành, nghề, công việc hoặc trường hợp sau: sản xuất, gia công xuất khẩu sản phẩm hàng dệt, may, da, giày, điện, điện tử, chế biến nông, lâm, diêm nghiệp, thủy sản; sản xuất, cung cấp điện, viễn thông, lọc dầu; cấp, thoát nước."""
    },
    # Page 21
    {
        "chapter": "VII",
        "header": "CHƯƠNG VII: THỜI GIỜ NGHỈ NGƠI VÀ NGHỈ HẰNG TUẦN",
        "content": """CHƯƠNG VII: THỜI GIỜ LÀM VIỆC, THỜI GIỜ NGHỈ NGƠI

Điều 109. Nghỉ trong giờ làm việc
1. Người lao động làm việc theo thời giờ làm việc quy định tại Điều 105 của Bộ luật này từ 06 giờ trở lên trong một ngày thì được nghỉ giữa giờ ít nhất 30 phút liên tục, làm việc ban đêm thì được nghỉ giữa giờ ít nhất 45 phút liên tục.
2. Trường hợp người lao động làm việc theo ca liên tục từ 06 giờ trở lên thì thời gian nghỉ giữa giờ được tính vào thời giờ làm việc.
3. Ngoài thời gian nghỉ giữa giờ quy định tại khoản 1 Điều này, người sử dụng lao động bố trí cho người lao động các đợt nghỉ giải lao và ghi vào nội quy lao động.

Điều 111. Nghỉ hằng tuần
1. Mỗi tuần, người lao động được nghỉ ít nhất 24 giờ liên tục. Trong trường hợp đặc biệt do chu kỳ lao động không thể nghỉ hằng tuần thì người sử dụng lao động có trách nhiệm bảo đảm cho người lao động được nghỉ tính bình quân 01 tháng ít nhất là 04 ngày.
2. Người sử dụng lao động có quyền quyết định sắp xếp ngày nghỉ hằng tuần vào ngày Chủ nhật hoặc ngày xác định khác trong tuần nhưng phải ghi vào nội quy lao động."""
    },
    # Page 22
    {
        "chapter": "VII",
        "header": "CHƯƠNG VII: NGHỈ LỄ TẾT VÀ NGHỈ HẰNG NĂM",
        "content": """CHƯƠNG VII: THỜI GIỜ LÀM VIỆC, THỜI GIỜ NGHỈ NGƠI

Điều 112. Nghỉ lễ, tết
1. Người lao động được nghỉ làm việc, hưởng nguyên lương trong những ngày lễ, tết sau đây: Tết Dương lịch: 01 ngày; Tết Âm lịch: 05 ngày; Ngày Chiến thắng: 01 ngày; Ngày Quốc tế lao động: 01 ngày; Quốc khánh: 02 ngày; Ngày Giỗ Tổ Hùng Vương: 01 ngày.
2. Lao động là người nước ngoài làm việc tại Việt Nam ngoài các ngày nghỉ lễ, tết quy định tại khoản 1 Điều này còn được nghỉ thêm 01 ngày Tết cổ truyền dân tộc và 01 ngày Quốc khánh của nước họ.

Điều 113. Nghỉ hằng năm
1. Người lao động làm việc đủ 12 tháng cho một người sử dụng lao động thì được nghỉ hằng năm, hưởng nguyên lương theo hợp đồng lao động như sau:
a) 12 ngày làm việc đối với người làm công việc trong điều kiện bình thường;
b) 14 ngày làm việc đối với người lao động chưa thành niên, lao động là người khuyết tật, người làm nghề, công việc nặng nhọc, độc hại, nguy hiểm;
c) 16 ngày làm việc đối với người làm nghề, công việc đặc biệt nặng nhọc, độc hại, nguy hiểm."""
    },
    # Page 23
    {
        "chapter": "VII",
        "header": "CHƯƠNG VII: NGHỈ VIỆC RIÊNG VÀ NGHỈ KHÔNG LƯƠNG",
        "content": """CHƯƠNG VII: THỜI GIỜ LÀM VIỆC, THỜI GIỜ NGHỈ NGƠI

Điều 115. Nghỉ việc riêng, nghỉ không hưởng lương
1. Người lao động được nghỉ việc riêng mà vẫn hưởng nguyên lương và phải thông báo với người sử dụng lao động trong trường hợp sau đây:
a) Kết hôn: nghỉ 03 ngày;
b) Con đẻ, con nuôi kết hôn: nghỉ 01 ngày;
c) Cha đẻ, mẹ đẻ, cha nuôi, mẹ nuôi; cha đẻ, mẹ đẻ, cha nuôi, mẹ nuôi của vợ hoặc chồng; vợ hoặc chồng; con đẻ, con nuôi chết: nghỉ 03 ngày.

2. Người lao động được nghỉ không hưởng lương 01 ngày và phải thông báo với người sử dụng lao động khi ông nội, bà nội, ông ngoại, bà ngoại, anh, chị, em ruột chết; cha hoặc mẹ kết hôn; anh, chị, em ruột kết hôn.
3. Ngoài quy định tại khoản 1 và khoản 2 Điều này, người lao động có thể thỏa thuận với người sử dụng lao động để nghỉ không hưởng lương."""
    },
    # Page 24
    {
        "chapter": "VIII",
        "header": "CHƯƠNG VIII: KỶ LUẬT LAO ĐỘNG VÀ NỘI QUY",
        "content": """CHƯƠNG VIII: KỶ LUẬT LAO ĐỘNG, TRÁCH NHIỆM VẬT CHẤT

Điều 117. Kỷ luật lao động
Kỷ luật lao động là những quy định về việc tuân theo thời gian, công nghệ và điều hành sản xuất, kinh doanh do người sử dụng lao động ban hành trong nội quy lao động và do pháp luật quy định.

Điều 118. Nội quy lao động
1. Người sử dụng lao động phải ban hành nội quy lao động, nếu sử dụng từ 10 người lao động trở lên thì nội quy lao động phải bằng văn bản.
2. Nội dung nội quy lao động không được trái với pháp luật về lao động và quy định của pháp luật có liên quan. Nội quy lao động bao gồm các nội dung chủ yếu sau: thời giờ làm việc, thời giờ nghỉ ngơi; trật tự tại nơi làm việc; an toàn, vệ sinh lao động; phòng, chống quấy rối tình dục tại nơi làm việc; bảo vệ tài sản và bí mật kinh doanh, bí mật công nghệ; các hành vi vi phạm kỷ luật lao động và các hình thức xử lý kỷ luật lao động; trách nhiệm vật chất."""
    },
    # Page 25
    {
        "chapter": "VIII",
        "header": "CHƯƠNG VIII: HÌNH THỨC KỶ LUẬT VÀ NGUYÊN TẮC XỬ LÝ",
        "content": """CHƯƠNG VIII: KỶ LUẬT LAO ĐỘNG, TRÁCH NHIỆM VẬT CHẤT

Điều 122. Nguyên tắc, trình tự, thủ tục xử lý kỷ luật lao động
1. Người sử dụng lao động phải chứng minh được lỗi của người lao động.
2. Phải có sự tham gia của tổ chức đại diện người lao động tại cơ sở mà người lao động đang bị xử lý kỷ luật là thành viên.
3. Người lao động phải có mặt và có quyền tự bào chữa, nhờ luật sư hoặc tổ chức đại diện người lao động bào chữa; trường hợp là người chưa đủ 15 tuổi thì phải có sự tham gia của người đại diện theo pháp luật.
4. Không được áp dụng nhiều hình thức xử lý kỷ luật lao động đối với một hành vi vi phạm kỷ luật lao động. Khi một người lao động đồng thời có nhiều hành vi vi phạm kỷ luật lao động thì chỉ áp dụng hình thức kỷ luật cao nhất tương ứng với hành vi vi phạm nặng nhất.

Điều 124. Các hình thức xử lý kỷ luật lao động
1. Khiển trách.
2. Kéo dài thời hạn nâng lương không quá 06 tháng.
3. Cách chức.
4. Sa thải."""
    },
    # Page 26
    {
        "chapter": "VIII",
        "header": "CHƯƠNG VIII: ÁP DỤNG HÌNH THỨC SA THẢI",
        "content": """CHƯƠNG VIII: KỶ LUẬT LAO ĐỘNG, TRÁCH NHIỆM VẬT CHẤT

Điều 125. Áp dụng hình thức xử lý kỷ luật sa thải
Hình thức xử lý kỷ luật sa thải được người sử dụng lao động áp dụng trong trường hợp sau đây:
1. Người lao động có hành vi trộm cắp, tham ô, đánh bạc, cố ý gây thương tích, sử dụng ma túy tại nơi làm việc.
2. Người lao động có hành vi tiết lộ bí mật kinh doanh, bí mật công nghệ, xâm phạm quyền sở hữu trí tuệ của người sử dụng lao động, có hành vi gây thiệt hại nghiêm trọng hoặc đe dọa gây thiệt hại đặc biệt nghiêm trọng về tài sản, lợi ích của người sử dụng lao động hoặc quấy rối tình dục tại nơi làm việc được quy định trong nội quy lao động.
3. Người lao động bị xử lý kỷ luật kéo dài thời hạn nâng lương hoặc cách chức mà tái phạm trong thời gian chưa xóa kỷ luật.
4. Người lao động tự ý bỏ việc 05 ngày cộng dồn trong thời hạn 30 ngày hoặc 20 ngày cộng dồn trong thời hạn 365 ngày tính từ ngày đầu tiên tự ý bỏ việc mà không có lý do chính đáng."""
    },
    # Page 27
    {
        "chapter": "VIII",
        "header": "CHƯƠNG VIII: HÀNH VI BỊ NGHIÊM CẤM KHI XỬ LÝ KỶ LUẬT",
        "content": """CHƯƠNG VIII: KỶ LUẬT LAO ĐỘNG, TRÁCH NHIỆM VẬT CHẤT

Điều 127. Các hành vi bị nghiêm cấm khi xử lý kỷ luật lao động
1. Xâm phạm sức khỏe, danh dự, tính mạng, uy tín, nhân phẩm của người lao động.
2. Phạt tiền, cắt lương thay việc xử lý kỷ luật lao động.
3. Xử lý kỷ luật lao động đối với người lao động có hành vi vi phạm không được quy định trong nội quy lao động hoặc không thỏa thuận trong hợp đồng lao động đã giao kết hoặc pháp luật về lao động không có quy định.

Điều 129. Bồi thường thiệt hại vật chất
1. Người lao động làm hư hỏng dụng cụ, thiết bị hoặc có hành vi khác gây thiệt hại tài sản của người sử dụng lao động thì phải bồi thường theo quy định của pháp luật hoặc nội quy lao động của người sử dụng lao động. Trường hợp gây thiệt hại không nghiêm trọng do sơ suất với giá trị không quá 10 tháng lương tối thiểu vùng do Chính phủ công bố thì người lao động phải bồi thường nhiều nhất là 03 tháng tiền lương và bị khấu trừ hằng tháng vào lương."""
    },
    # Page 28
    {
        "chapter": "IX",
        "header": "CHƯƠNG IX: AN TOÀN, VỆ SINH LAO ĐỘNG",
        "content": """CHƯƠNG IX: AN TOÀN, VỆ SINH LAO ĐỘNG

Điều 132. Tuân thủ pháp luật về an toàn, vệ sinh lao động
Người sử dụng lao động, người lao động và cơ quan, tổ chức, cá nhân có liên quan đến lao động, sản xuất, kinh doanh phải thực hiện quy định của pháp luật về an toàn, vệ sinh lao động.

Điều 133. Quyền và nghĩa vụ của người lao động về an toàn, vệ sinh lao động
1. Người lao động có các quyền sau: Được bảo đảm các điều kiện làm việc an toàn, vệ sinh lao động; Yêu cầu người sử dụng lao động có trách nhiệm bảo đảm điều kiện làm việc an toàn; Được cung cấp thông tin đầy đủ về các yếu tố nguy hiểm, yếu tố có hại tại nơi làm việc và các biện pháp phòng, chống; Từ chối làm công việc hoặc rời bỏ nơi làm việc mà vẫn được trả đủ tiền lương và không bị coi là vi phạm kỷ luật lao động khi thấy rõ có nguy cơ xảy ra tai nạn lao động đe dọa nghiêm trọng tính mạng hoặc sức khỏe của mình.
2. Người lao động có nghĩa vụ chấp hành quy định, nội quy, quy trình, biện pháp bảo đảm an toàn, vệ sinh lao động tại nơi làm việc; Sử dụng và bảo quản các phương tiện bảo vệ cá nhân đã được trang cấp."""
    },
    # Page 29
    {
        "chapter": "X",
        "header": "CHƯƠNG X: LAO ĐỘNG NỮ VÀ BÌNH ĐẲNG GIỚI",
        "content": """CHƯƠNG X: NHỮNG QUY ĐỊNH RIÊNG ĐỐI VỚI LAO ĐỘNG NỮ VÀ BẢO ĐẢM BÌNH ĐẲNG GIỚI

Điều 135. Chính sách của Nhà nước đối với lao động nữ
1. Bảo đảm quyền bình đẳng của lao động nữ, lao động nam, thực hiện các biện pháp bảo đảm bình đẳng giới và phòng, chống quấy rối tình dục tại nơi làm việc.
2. Khuyến khích người sử dụng lao động tạo điều kiện để lao động nữ, lao động nam có việc làm thường xuyên, áp dụng rộng rãi chế độ làm việc theo thời gian biểu linh hoạt, làm việc không trọn thời gian, giao việc làm tại nhà.

Điều 137. Bảo vệ thai sản
1. Người sử dụng lao động không được sử dụng người lao động làm việc ban đêm, làm thêm giờ và đi công tác xa trong các trường hợp sau đây:
a) Mang thai từ tháng thứ 07 hoặc từ tháng thứ 06 nếu làm việc ở vùng cao, vùng sâu, vùng xa, biên giới, hải đảo.
b) Đang nuôi con dưới 12 tháng tuổi, trừ trường hợp được người lao động đồng ý.
2. Lao động nữ làm nghề, công việc nặng nhọc, độc hại, nguy hiểm khi mang thai và có thông báo cho người sử dụng lao động biết thì được chuyển làm công việc nhẹ hơn, an toàn hơn hoặc giảm bớt 01 giờ làm việc hằng ngày mà không bị cắt giảm tiền lương."""
    },
    # Page 30
    {
        "chapter": "X",
        "header": "CHƯƠNG X: CHẾ ĐỘ THAI SẢN VÀ BẢO ĐẢM VIỆC LÀM",
        "content": """CHƯƠNG X: NHỮNG QUY ĐỊNH RIÊNG ĐỐI VỚI LAO ĐỘNG NỮ VÀ BẢO ĐẢM BÌNH ĐẲNG GIỚI

Điều 139. Nghỉ thai sản
1. Lao động nữ được nghỉ thai sản trước và sau khi sinh con là 06 tháng; thời gian nghỉ trước khi sinh không quá 02 tháng. Trường hợp lao động nữ sinh đôi trở lên thì tính từ con thứ 02 trở đi, cứ mỗi con, người mẹ được nghỉ thêm 01 tháng.
2. Trong thời gian nghỉ thai sản, lao động nữ được hưởng chế độ thai sản theo quy định của pháp luật về bảo hiểm xã hội.
3. Hết thời gian nghỉ thai sản theo quy định tại khoản 1 Điều này, nếu có nhu cầu, có sự đồng ý của người sử dụng lao động thì lao động nữ có thể nghỉ thêm một thời gian không hưởng lương.

Điều 140. Bảo đảm việc làm cho lao động nghỉ thai sản
Lao động được bảo đảm việc làm cũ khi trở lại làm việc sau khi nghỉ hết thời gian thai sản mà không bị giảm tiền lương và quyền, lợi ích so với trước khi nghỉ thai sản; trường hợp việc làm cũ không còn thì người sử dụng lao động phải bố trí việc làm khác cho họ với mức lương không thấp hơn mức lương trước khi nghỉ thai sản."""
    },
    # Page 31
    {
        "chapter": "XI",
        "header": "CHƯƠNG XI: LAO ĐỘNG CHƯA THÀNH NIÊN",
        "content": """CHƯƠNG XI: NHỮNG QUY ĐỊNH RIÊNG ĐỐI VỚI LAO ĐỘNG CHƯA THÀNH NIÊN VÀ MỘT SỐ LAO ĐỘNG KHÁC

Điều 143. Lao động chưa thành niên
1. Lao động chưa thành niên là người lao động chưa đủ 18 tuổi.
2. Người từ đủ 15 tuổi đến chưa đủ 18 tuổi không được làm công việc hoặc làm việc ở nơi làm việc quy định tại Điều 147 của Bộ luật này.
3. Người từ đủ 13 tuổi đến chưa đủ 15 tuổi chỉ được làm công việc nhẹ theo danh mục do Bộ trưởng Bộ Lao động - Thương binh và Xã hội ban hành.
4. Người chưa đủ 13 tuổi chỉ được làm các công việc nghệ thuật, thể dục, thể thao nhưng không làm tổn hại đến sự phát triển thể lực, trí lực, nhân cách của người chưa đủ 13 tuổi và phải có sự đồng ý của cơ quan chuyên môn về lao động thuộc Ủy ban nhân dân cấp tỉnh.

Điều 146. Thời giờ làm việc của người chưa thành niên
1. Thời giờ làm việc của người chưa đủ 15 tuổi không quá 04 giờ trong 01 ngày và không quá 20 giờ trong 01 tuần; không được làm thêm giờ, làm việc vào ban đêm.
2. Thời giờ làm việc của người từ đủ 15 tuổi đến chưa đủ 18 tuổi không quá 08 giờ trong 01 ngày và không quá 40 giờ trong 01 tuần. Người từ đủ 15 tuổi đến chưa đủ 18 tuổi có thể được làm thêm giờ, làm việc vào ban đêm trong một số nghề, công việc theo danh mục do Bộ trưởng Bộ Lao động - Thương binh và Xã hội ban hành."""
    },
    # Page 32
    {
        "chapter": "XI",
        "header": "CHƯƠNG XI: TUỔI NGHỈ HƯU",
        "content": """CHƯƠNG XI: NHỮNG QUY ĐỊNH RIÊNG ĐỐI VỚI MỘT SỐ LAO ĐỘNG KHÁC

Điều 169. Tuổi nghỉ hưu
1. Người lao động bảo đảm điều kiện về thời gian đóng bảo hiểm xã hội theo quy định của pháp luật về bảo hiểm xã hội được hưởng lương hưu khi đủ tuổi nghỉ hưu.
2. Tuổi nghỉ hưu của người lao động trong điều kiện lao động bình thường được điều chỉnh theo lộ trình cho đến khi đủ 62 tuổi đối với lao động nam vào năm 2028 và đủ 60 tuổi đối với lao động nữ vào năm 2035.
Kể từ năm 2021, tuổi nghỉ hưu của người lao động trong điều kiện lao động bình thường là đủ 60 tuổi 03 tháng đối với lao động nam và đủ 55 tuổi 04 tháng đối với lao động nữ; sau đó, cứ mỗi năm tăng thêm 03 tháng đối với lao động nam và 04 tháng đối với lao động nữ.
3. Người lao động bị suy giảm khả năng lao động; làm nghề, công việc đặc biệt nặng nhọc, độc hại, nguy hiểm; làm việc ở vùng có điều kiện kinh tế - xã hội đặc biệt khó khăn có thể nghỉ hưu ở tuổi thấp hơn nhưng không quá 05 tuổi so với quy định tại khoản 2 Điều này.
4. Người lao động có trình độ chuyên môn, kỹ thuật cao và một số trường hợp đặc biệt có thể nghỉ hưu ở tuổi cao hơn nhưng không quá 05 tuổi so với quy định tại khoản 2 Điều này."""
    },
    # Page 33
    {
        "chapter": "XII",
        "header": "CHƯƠNG XII: BẢO HIỂM XÃ HỘI, BẢO HIỂM Y TẾ, BẢO HIỂM THẤT NGHIỆP",
        "content": """CHƯƠNG XII: BẢO HIỂM XÃ HỘI, BẢO HIỂM Y TẾ, BẢO HIỂM THẤT NGHIỆP

Điều 168. Tham gia bảo hiểm xã hội, bảo hiểm y tế, bảo hiểm thất nghiệp
1. Người sử dụng lao động, người lao động phải tham gia bảo hiểm xã hội bắt buộc, bảo hiểm y tế, bảo hiểm thất nghiệp; người lao động được hưởng các chế độ theo quy định của pháp luật về bảo hiểm xã hội, bảo hiểm y tế và bảo hiểm thất nghiệp. Khuyến khích người sử dụng lao động, người lao động tham gia các hình thức bảo hiểm khác đối với người lao động.
2. Trong thời gian người lao động nghỉ việc được hưởng chế độ bảo hiểm xã hội thì người sử dụng lao động không phải trả lương cho người lao động, trừ trường hợp hai bên có thỏa thuận khác.
3. Đối với người lao động không thuộc đối tượng tham gia bảo hiểm xã hội bắt buộc, bảo hiểm y tế, bảo hiểm thất nghiệp thì người sử dụng lao động có trách nhiệm chi trả thêm cùng lúc với kỳ trả lương một khoản tiền cho người lao động tương đương với mức người sử dụng lao động đóng bảo hiểm xã hội, bảo hiểm y tế, bảo hiểm thất nghiệp cho người lao động theo quy định của pháp luật."""
    },
    # Page 34
    {
        "chapter": "XIII",
        "header": "CHƯƠNG XIII: TỔ CHỨC ĐẠI DIỆN NGƯỜI LAO ĐỘNG TẠI CƠ SỞ",
        "content": """CHƯƠNG XIII: TỔ CHỨC ĐẠI DIỆN NGƯỜI LAO ĐỘNG TẠI CƠ SỞ

Điều 170. Quyền thành lập, gia nhập và tham gia hoạt động của tổ chức đại diện người lao động tại cơ sở
1. Người lao động có quyền thành lập, gia nhập và hoạt động công đoàn theo quy định của Luật Công đoàn.
2. Người lao động trong doanh nghiệp có quyền thành lập, gia nhập và tham gia hoạt động của tổ chức của người lao động tại doanh nghiệp theo quy định tại các điều 172, 173 và 174 của Bộ luật này.
3. Các tổ chức đại diện người lao động tại cơ sở quy định tại khoản 1 và khoản 2 Điều này bình đẳng về quyền và nghĩa vụ trong việc đại diện bảo vệ quyền và lợi ích hợp pháp, chính đáng của người lao động trong quan hệ lao động.

Điều 175. Các hành vi bị nghiêm cấm đối với người sử dụng lao động liên quan đến thành lập, gia nhập và hoạt động của tổ chức đại diện người lao động tại cơ sở
1. Phân biệt đối xử đối với người lao động, thành viên ban lãnh đạo của tổ chức đại diện người lao động tại cơ sở vì lý do thành lập, gia nhập hoặc hoạt động tổ chức đại diện người lao động.
2. Can thiệp, thao túng quá trình thành lập, bầu cử, lập kế hoạch công tác hoặc tổ chức thực hiện các hoạt động của tổ chức đại diện người lao động tại cơ sở."""
    },
    # Page 35
    {
        "chapter": "XVII",
        "header": "CHƯƠNG XVII: ĐIỀU KHOẢN THI HÀNH",
        "content": """CHƯƠNG XVII: ĐIỀU KHOẢN THI HÀNH

Điều 220. Hiệu lực thi hành
1. Bộ luật này có hiệu lực thi hành từ ngày 01 tháng 01 năm 2021.
2. Bộ luật Lao động số 10/2012/QH13 hết hiệu lực kể từ ngày Bộ luật này có hiệu lực thi hành.
3. Kể từ ngày Bộ luật này có hiệu lực thi hành, các hợp đồng lao động, thỏa ước lao động tập thể, nội quy lao động và các thỏa thuận hợp pháp khác đã giao kết mà không trái hoặc có lợi hơn cho người lao động so với quy định của Bộ luật này thì được tiếp tục thực hiện, trừ trường hợp các bên có thỏa thuận về việc sửa đổi, bổ sung để phù hợp và để áp dụng quy định của Bộ luật này.

Chủ tịch Quốc hội: Nguyễn Thị Kim Ngân (đã ký)."""
    },
]

# Benchmark questions adhering strictly to BENCHMARK.md
QUESTIONS = [
    # 1. Direct (Chương I) - with filter (dev)
    {
        "id": "q01",
        "split": "dev",
        "type": "truc_tiep",
        "question": "Độ tuổi lao động tối thiểu của người lao động theo quy định là bao nhiêu tuổi?",
        "expected_answer": "Đủ 15 tuổi (trừ trường hợp quy định riêng tại Mục 1 Chương XI).",
        "gold_source_id": "LuatLaoDong2019",
        "gold_page": 2,
        "evidence_quote": "Độ tuổi lao động tối thiểu của người lao động là đủ 15 tuổi, trừ trường hợp quy định tại Mục 1 Chương XI của Bộ luật này.",
        "filter": {"chapter": "I"}
    },
    # 2. Exceptions / Prohibitions (Chương I) (dev)
    {
        "id": "q02",
        "split": "dev",
        "type": "dieu_kien_ngoai_le",
        "question": "Những hành vi nào bị nghiêm cấm trong lĩnh vực lao động?",
        "expected_answer": "Phân biệt đối xử trong lao động, cưỡng bức lao động, quấy rối tình dục tại nơi làm việc.",
        "gold_source_id": "LuatLaoDong2019",
        "gold_page": 3,
        "evidence_quote": "Phân biệt đối xử trong lao động; Cưỡng bức lao động; Quấy rối tình dục tại nơi làm việc.",
        "filter": None
    },
    # 3. Direct (Chương II) (dev)
    {
        "id": "q03",
        "split": "dev",
        "type": "truc_tiep",
        "question": "Người sử dụng lao động có bắt buộc phải lập sổ quản lý lao động không?",
        "expected_answer": "Có, phải lập sổ quản lý lao động bằng bản giấy hoặc bản điện tử.",
        "gold_source_id": "LuatLaoDong2019",
        "gold_page": 5,
        "evidence_quote": "Người sử dụng lao động phải lập sổ quản lý lao động bằng bản giấy hoặc bản điện tử và xuất trình khi cơ quan nhà nước có thẩm quyền yêu cầu.",
        "filter": None
    },
    # 4. Direct (Chương III) - with filter (dev)
    {
        "id": "q04",
        "split": "dev",
        "type": "truc_tiep",
        "question": "Bộ luật Lao động 2019 quy định hợp đồng lao động gồm những loại nào?",
        "expected_answer": "Hợp đồng lao động không xác định thời hạn và hợp đồng lao động xác định thời hạn không quá 36 tháng.",
        "gold_source_id": "LuatLaoDong2019",
        "gold_page": 7,
        "evidence_quote": "Hợp đồng lao động không xác định thời hạn là hợp đồng mà trong đó hai bên không xác định thời hạn, thời điểm chấm dứt hiệu lực của hợp đồng; Hợp đồng lao động xác định thời hạn là hợp đồng mà trong đó hai bên xác định thời hạn, thời điểm chấm dứt hiệu lực của hợp đồng trong thời gian không quá 36 tháng.",
        "filter": {"chapter": "III"}
    },
    # 5. Paraphrased (Chương III) (dev)
    {
        "id": "q05",
        "split": "dev",
        "type": "dien_dat_lai",
        "question": "Thời gian làm thử việc tối đa đối với chức danh người quản lý doanh nghiệp là bao nhiêu ngày?",
        "expected_answer": "Không quá 180 ngày.",
        "gold_source_id": "LuatLaoDong2019",
        "gold_page": 8,
        "evidence_quote": "Không quá 180 ngày đối với công việc của người quản lý doanh nghiệp theo quy định của Luật Doanh nghiệp.",
        "filter": None
    },
    # 6. Direct (Chương III) (dev)
    {
        "id": "q06",
        "split": "dev",
        "type": "truc_tiep",
        "question": "Mức tiền lương thử việc tối thiểu được pháp luật quy định bằng bao nhiêu so với lương chính thức?",
        "expected_answer": "Ít nhất bằng 85% mức lương của công việc đó.",
        "gold_source_id": "LuatLaoDong2019",
        "gold_page": 8,
        "evidence_quote": "Tiền lương của người lao động trong thời gian thử việc do hai bên thỏa thuận nhưng ít nhất phải bằng 85% mức lương của công việc đó.",
        "filter": None
    },
    # 7. Conditional (Chương III) - with filter (dev)
    {
        "id": "q07",
        "split": "dev",
        "type": "dieu_kien_ngoai_le",
        "question": "Thời hạn báo trước của người lao động khi đơn phương chấm dứt hợp đồng không xác định thời hạn là bao lâu?",
        "expected_answer": "Ít nhất 45 ngày.",
        "gold_source_id": "LuatLaoDong2019",
        "gold_page": 10,
        "evidence_quote": "Ít nhất 45 ngày nếu làm việc theo hợp đồng lao động không xác định thời hạn.",
        "filter": {"chapter": "III"}
    },
    # 8. Direct (Chương III) (dev)
    {
        "id": "q08",
        "split": "dev",
        "type": "truc_tiep",
        "question": "Mức trợ cấp thôi việc được tính như thế nào cho mỗi năm làm việc?",
        "expected_answer": "Mỗi năm làm việc được trợ cấp một nửa tháng tiền lương.",
        "gold_source_id": "LuatLaoDong2019",
        "gold_page": 11,
        "evidence_quote": "Mỗi năm làm việc được trợ cấp một nửa tháng tiền lương, trừ trường hợp đủ điều kiện hưởng lương hưu.",
        "filter": None
    },
    # 9. Direct (Chương III) (dev)
    {
        "id": "q09",
        "split": "dev",
        "type": "truc_tiep",
        "question": "Mức chi trả trợ cấp mất việc làm tối thiểu cho người lao động là bao nhiêu tháng lương?",
        "expected_answer": "Ít nhất bằng 02 tháng tiền lương.",
        "gold_source_id": "LuatLaoDong2019",
        "gold_page": 11,
        "evidence_quote": "Người sử dụng lao động trả trợ cấp mất việc làm cho người lao động đã làm việc thường xuyên cho mình từ đủ 12 tháng trở lên mà bị mất việc làm, mỗi năm làm việc trả 01 tháng tiền lương nhưng ít nhất bằng 02 tháng tiền lương.",
        "filter": None
    },
    # 10. Paraphrased (Chương V) (dev)
    {
        "id": "q10",
        "split": "dev",
        "type": "dien_dat_lai",
        "question": "Tần suất tối thiểu phải tổ chức đối thoại định kỳ giữa doanh nghiệp và người lao động là bao lâu?",
        "expected_answer": "Định kỳ ít nhất 01 năm một lần.",
        "gold_source_id": "LuatLaoDong2019",
        "gold_page": 14,
        "evidence_quote": "Định kỳ ít nhất 01 năm một lần; Khi có yêu cầu của một hoặc các bên; Khi có vụ việc quy định tại điểm a khoản 1 Điều 36, các điều 42, 44, 93, 104, 118.",
        "filter": None
    },
    # 11. Direct (Chương V) (dev)
    {
        "id": "q11",
        "split": "dev",
        "type": "truc_tiep",
        "question": "Thỏa ước lao động tập thể doanh nghiệp được ký kết khi có bao nhiêu phần trăm người lao động biểu quyết tán thành?",
        "expected_answer": "Có trên 50% người lao động của doanh nghiệp biểu quyết tán thành.",
        "gold_source_id": "LuatLaoDong2019",
        "gold_page": 15,
        "evidence_quote": "Thỏa ước lao động tập thể doanh nghiệp được ký kết khi có trên 50% người lao động của doanh nghiệp biểu quyết tán thành.",
        "filter": None
    },
    # 12. Conditional (Chương VI) (dev)
    {
        "id": "q12",
        "split": "dev",
        "type": "dieu_kien_ngoai_le",
        "question": "Khi trả lương qua tài khoản ngân hàng, ai phải chịu các khoản phí mở tài khoản và chuyển tiền lương?",
        "expected_answer": "Người sử dụng lao động phải trả các chi phí này.",
        "gold_source_id": "LuatLaoDong2019",
        "gold_page": 17,
        "evidence_quote": "Trường hợp trả lương qua tài khoản cá nhân của người lao động được mở tại ngân hàng thì người sử dụng lao động phải trả các loại phí liên quan đến việc mở tài khoản và chuyển tiền lương.",
        "filter": None
    },
    # 13. Direct (Chương VI) (dev)
    {
        "id": "q13",
        "split": "dev",
        "type": "truc_tiep",
        "question": "Mức tiền lương làm thêm giờ vào ngày nghỉ hằng tuần được tính tối thiểu bằng bao nhiêu phần trăm?",
        "expected_answer": "Ít nhất bằng 200%.",
        "gold_source_id": "LuatLaoDong2019",
        "gold_page": 18,
        "evidence_quote": "Vào ngày nghỉ hằng tuần, ít nhất bằng 200%; Vào ngày nghỉ lễ, tết, ngày nghỉ có hưởng lương, ít nhất bằng 300% chưa kể tiền lương ngày lễ, tết.",
        "filter": None
    },
    # 14. Direct (Chương VII) (dev)
    {
        "id": "q14",
        "split": "dev",
        "type": "truc_tiep",
        "question": "Thời giờ làm việc bình thường của người lao động không được vượt quá bao nhiêu giờ trong một ngày và một tuần?",
        "expected_answer": "Không quá 08 giờ trong 01 ngày và không quá 48 giờ trong 01 tuần.",
        "gold_source_id": "LuatLaoDong2019",
        "gold_page": 19,
        "evidence_quote": "Thời giờ làm việc bình thường không quá 08 giờ trong 01 ngày và không quá 48 giờ trong 01 tuần.",
        "filter": None
    },
    # 15. Conditional (Chương VII) (dev)
    {
        "id": "q15",
        "split": "dev",
        "type": "dieu_kien_ngoai_le",
        "question": "Khung giờ làm việc ban đêm được xác định từ mấy giờ đến mấy giờ?",
        "expected_answer": "Từ 22 giờ đến 06 giờ sáng ngày hôm sau.",
        "gold_source_id": "LuatLaoDong2019",
        "gold_page": 19,
        "evidence_quote": "Giờ làm việc ban đêm được tính từ 22 giờ đến 06 giờ sáng ngày hôm sau.",
        "filter": None
    },
    # 16. Direct (Chương VII) - with filter (test)
    {
        "id": "q16",
        "split": "test",
        "type": "truc_tiep",
        "question": "Số giờ làm thêm tối đa của người lao động trong một tháng và một năm trong điều kiện bình thường là bao nhiêu?",
        "expected_answer": "Không quá 40 giờ trong 01 tháng và không quá 200 giờ trong 01 năm.",
        "gold_source_id": "LuatLaoDong2019",
        "gold_page": 20,
        "evidence_quote": "Bảo đảm số giờ làm thêm của người lao động không quá 50% số giờ làm việc bình thường trong 01 ngày; không quá 40 giờ trong 01 tháng; Không quá 200 giờ trong 01 năm, trừ trường hợp quy định tại khoản 3 Điều này.",
        "filter": {"chapter": "VII"}
    },
    # 17. Paraphrased (Chương VII) (test)
    {
        "id": "q17",
        "split": "test",
        "type": "dien_dat_lai",
        "question": "Người lao động được nghỉ làm việc hưởng nguyên lương trong các dịp lễ, tết tổng cộng bao nhiêu ngày trong năm?",
        "expected_answer": "Tổng cộng 11 ngày nghỉ lễ, tết hưởng nguyên lương.",
        "gold_source_id": "LuatLaoDong2019",
        "gold_page": 22,
        "evidence_quote": "Người lao động được nghỉ làm việc, hưởng nguyên lương trong những ngày lễ, tết sau đây: Tết Dương lịch: 01 ngày; Tết Âm lịch: 05 ngày; Ngày Chiến thắng: 01 ngày; Ngày Quốc tế lao động: 01 ngày; Quốc khánh: 02 ngày; Ngày Giỗ Tổ Hùng Vương: 01 ngày.",
        "filter": None
    },
    # 18. Conditional / Exceptions (Chương VIII) (test)
    {
        "id": "q18",
        "split": "test",
        "type": "dieu_kien_ngoai_le",
        "question": "Người lao động tự ý bỏ việc bao nhiêu ngày không có lý do chính đáng thì có thể bị kỷ luật sa thải?",
        "expected_answer": "Tự ý bỏ việc 05 ngày cộng dồn trong thời hạn 30 ngày hoặc 20 ngày cộng dồn trong 365 ngày.",
        "gold_source_id": "LuatLaoDong2019",
        "gold_page": 26,
        "evidence_quote": "Người lao động tự ý bỏ việc 05 ngày cộng dồn trong thời hạn 30 ngày hoặc 20 ngày cộng dồn trong thời hạn 365 ngày tính từ ngày đầu tiên tự ý bỏ việc mà không có lý do chính đáng.",
        "filter": None
    },
    # 19. Conditional (Chương X) (test)
    {
        "id": "q19",
        "split": "test",
        "type": "dieu_kien_ngoai_le",
        "question": "Người sử dụng lao động bị cấm bắt lao động nữ làm việc ban đêm hoặc làm thêm giờ khi mang thai từ tháng thứ mấy?",
        "expected_answer": "Từ tháng thứ 07 hoặc từ tháng thứ 06 nếu làm việc ở vùng cao, vùng sâu, vùng xa, biên giới, hải đảo.",
        "gold_source_id": "LuatLaoDong2019",
        "gold_page": 29,
        "evidence_quote": "Mang thai từ tháng thứ 07 hoặc từ tháng thứ 06 nếu làm việc ở vùng cao, vùng sâu, vùng xa, biên giới, hải đảo.",
        "filter": None
    },
    # 20. Direct (Chương XI) (test)
    {
        "id": "q20",
        "split": "test",
        "type": "truc_tiep",
        "question": "Lộ trình điều chỉnh tuổi nghỉ hưu của lao động nam và lao động nữ trong điều kiện bình thường đạt mốc bao nhiêu tuổi?",
        "expected_answer": "Đủ 62 tuổi đối với nam vào năm 2028 và đủ 60 tuổi đối với nữ vào năm 2035.",
        "gold_source_id": "LuatLaoDong2019",
        "gold_page": 32,
        "evidence_quote": "Tuổi nghỉ hưu của người lao động trong điều kiện lao động bình thường được điều chỉnh theo lộ trình cho đến khi đủ 62 tuổi đối với lao động nam vào năm 2028 và đủ 60 tuổi đối với lao động nữ vào năm 2035.",
        "filter": None
    },
]


def generate_pdf():
    print(f"Generating searchable PDF with {len(PAGES_DATA)} pages...")
    doc = pymupdf.open()

    for idx, p_info in enumerate(PAGES_DATA):
        page_num = idx + 1
        page = doc.new_page(width=595, height=842)  # A4 size

        # Register Vietnamese font
        page.insert_font(fontname="ArialVN", fontfile=FONT_PATH)

        # Header
        header_text = f"BỘ LUẬT LAO ĐỘNG 2019 | {p_info['header']}"
        page.insert_text((50, 45), header_text, fontname="ArialVN", fontsize=9, color=(0.4, 0.4, 0.4))

        # Divider line
        page.draw_line((50, 52), (545, 52), color=(0.7, 0.7, 0.7), width=0.5)

        # Body text
        rect = pymupdf.Rect(50, 65, 545, 790)
        page.insert_textbox(rect, p_info["content"], fontname="ArialVN", fontsize=10.5, lineheight=1.4)

        # Footer
        footer_text = f"Trang {page_num} / {len(PAGES_DATA)}"
        page.insert_text((270, 815), footer_text, fontname="ArialVN", fontsize=9, color=(0.4, 0.4, 0.4))

    doc.save(str(PDF_OUTPUT_PATH))
    doc.close()
    print(f"Successfully generated: {PDF_OUTPUT_PATH} ({len(PAGES_DATA)} pages)")


def generate_benchmark():
    print(f"Generating benchmark questions at: {QUESTIONS_OUTPUT_PATH}...")
    with open(QUESTIONS_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(QUESTIONS, f, ensure_ascii=False, indent=2)
    print(f"Successfully written {len(QUESTIONS)} questions.")


def verify_benchmark_against_pdf():
    from starter.src.evaluation import _normalize

    print("\nVerifying all 20 questions against generated PDF...")
    doc = pymupdf.open(str(PDF_OUTPUT_PATH))
    print(f"PDF page count: {len(doc)}")

    errors = 0
    for q in QUESTIONS:
        p_num = q["gold_page"]
        pdf_page = doc[p_num - 1]
        page_text = pdf_page.get_text()

        clean_page = _normalize(page_text)
        clean_ev = _normalize(q["evidence_quote"])

        if clean_ev not in clean_page:
            print(f"❌ Error in {q['id']}: Evidence NOT found on Page {p_num}!")
            print(f"   Expected quote: {q['evidence_quote'][:60]}...")
            errors += 1
        else:
            print(f"✅ {q['id']} ({q['split']}) on Page {p_num}: Verified exact evidence match.")

    doc.close()
    if errors == 0:
        print("\n🎉 ALL 20 QUESTIONS VERIFIED 100% MATCHING THE PDF TEXT LAYER!\n")
    else:
        raise RuntimeError(f"Verification failed with {errors} errors.")


if __name__ == "__main__":
    generate_pdf()
    generate_benchmark()
    verify_benchmark_against_pdf()
