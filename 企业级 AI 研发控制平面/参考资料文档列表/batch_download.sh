#!/bin/bash
# 批量下载微信文章为PDF

OUTPUT_DIR="/Users/lizhenwei/Downloads/00download/docs/企业级 AI 研发控制平面/参考资料文档列表/pdfs"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# 定义文章列表（序号:URL）
declare -A articles
articles[1]="https://mp.weixin.qq.com/s/gs5ndvlMqM-Y4jg1_D2aFw"
articles[2]="https://mp.weixin.qq.com/s?__biz=Mzg2MzcyODQ5MQ==&mid=2247500767&idx=1&sn=b3d620a57e8833c4928da40f67fdecd1"
articles[3]="https://mp.weixin.qq.com/s?__biz=MzIzNjE2NTI3NQ==&mid=2247491737&idx=1&sn=7540894e1d73a1cf20da8e34ba421634"
articles[4]="https://mp.weixin.qq.com/s?__biz=MzI2NDU4OTExOQ==&mid=2247695294&idx=1&sn=63a246504edde73b337f15ad72bed3b1"
articles[5]="https://mp.weixin.qq.com/s?__biz=MzA3MjQyODkzOA==&mid=2448563920&idx=1&sn=94da4bd0f27dd31c20fc65aa6c858ad5"
articles[6]="https://mp.weixin.qq.com/s?__biz=Mzg5ODkxNjkxMw==&mid=2247483876&idx=1&sn=105736f125ec1a08296142f4e50df7ec"
articles[7]="https://mp.weixin.qq.com/s?__biz=MzA4NzgzMjA4MQ==&mid=2453482197&idx=1&sn=2116771a02c3c1f322532429daa1f0b6"
articles[8]="https://mp.weixin.qq.com/s?__biz=MzA4NzgzMjA4MQ==&mid=2453483103&idx=1&sn=559d2c07cadcef99051c77e38e3cfe29"
articles[9]="https://mp.weixin.qq.com/s?t=pages/image_detail&scene=1&__biz=MzkzNDkyNTQ5Ng==&mid=2247483687&idx=1&sn=fef1a688d1b222ca1792c1013d96b31a"
articles[10]="https://mp.weixin.qq.com/s?__biz=MzYzMTAxNTQ2Mg==&mid=2247483778&idx=1&sn=d63150d510f3e30fbc567e2f2342efa6"
articles[11]="https://mp.weixin.qq.com/s?__biz=MzE5ODExMjI3Mw==&mid=2247487831&idx=1&sn=f4d5b3d7f4f94f07d0b8b84a69ff6f50"
articles[12]="https://mp.weixin.qq.com/s?t=pages/image_detail&scene=1&__biz=MzkzNDkyNTQ5Ng==&mid=2247483677&idx=1&sn=e285d15f885ba90083878e2cc58b215a"
articles[13]="https://mp.weixin.qq.com/s?__biz=MzI2NDU4OTExOQ==&mid=2247695259&idx=1&sn=30ef327bcbbb3e349abd812da627c5f2"
articles[14]="https://mp.weixin.qq.com/s?t=pages/image_detail&scene=1&__biz=MzI2MDg3Njk0OA==&mid=2247489328&idx=1&sn=7d46f1791eb4e510fda0020849e9ee18"
articles[15]="https://mp.weixin.qq.com/s?__biz=MzIzOTU0NTQ0MA==&mid=2247559661&idx=1&sn=ca9426f948819f172ec44f671127aa29"
articles[16]="https://mp.weixin.qq.com/s?t=pages/image_detail&scene=1&__biz=MzAxOTUwMTY5Mw==&mid=2247484820&idx=1&sn=440d5c1718eb6efc7a6fdb90c78c7cf2"
articles[17]="https://mp.weixin.qq.com/s?__biz=Mzg3ODU0NDA2OA==&mid=2247485393&idx=1&sn=1ec35238386026af259796cf964a35f6"
articles[18]="https://mp.weixin.qq.com/s?t=pages/image_detail&scene=1&__biz=MzkxOTQwMDgyOQ==&mid=2247488816&idx=1&sn=737d262ca227995e2e1beefd12ada8bf"
articles[19]="https://mp.weixin.qq.com/s?__biz=MzI4MTA0NzkxMA==&mid=2648896698&idx=1&sn=966f92bb4fa66268fc15cb82cc2a7fb3"
articles[20]="https://mp.weixin.qq.com/s?t=pages/image_detail&scene=1&__biz=MzA3OTIwMDY0MQ==&mid=2247485174&idx=1&sn=c99811a6be03fdbfa45ea8cd16acfc9e"
articles[21]="https://mp.weixin.qq.com/s?t=pages/image_detail&scene=1&__biz=Mzg4MDYzNjM5OQ==&mid=2247489450&idx=1&sn=1e7784b89fdd84dc65e5cdc52307bfba"
articles[22]="https://mp.weixin.qq.com/s?__biz=MzA4Mzc5ODAwMA==&mid=2247490437&idx=1&sn=3b75734e1438cb64aaaf247aa9ac4943"
articles[23]="https://mp.weixin.qq.com/s?t=pages/image_detail&scene=1&__biz=MzYzNTU4NzkyOA==&mid=2247484160&idx=1&sn=a33101d6d37ab3fae2a381daf499f1ea"
articles[24]="https://mp.weixin.qq.com/s?t=pages/image_detail&scene=1&__biz=MzUxMjYzMzMyNg==&mid=2247484211&idx=1&sn=f64e69f90008582d7efdbe448fce5021"
articles[25]="https://mp.weixin.qq.com/s?t=pages/image_detail&scene=1&__biz=MzAxMzQyMzU5Nw==&mid=2454197363&idx=1&sn=84453bc2c1037546680b43574311d5bc"
articles[26]="https://mp.weixin.qq.com/s?__biz=MzE5ODQyNDY4OQ==&mid=2247484270&idx=1&sn=bfc5640a9c575404b6b154ccffe9ca87"
articles[27]="https://mp.weixin.qq.com/s?t=pages/image_detail&scene=1&__biz=MzkyNzcyMzcxOQ==&mid=2247484514&idx=1&sn=d53e155829db7a0307971d244562f7b6"
articles[28]="https://mp.weixin.qq.com/s?__biz=MzUyNTE2MDc1OA==&mid=2247485243&idx=1&sn=0ceba07c79448af5e75fc189aae5cf64"
articles[29]="https://mp.weixin.qq.com/s?__biz=Mzg3NzI0MzAyNA==&mid=2247492815&idx=1&sn=0dccd0f6f990aadf43d069d167ca4ca9"
articles[30]="https://mp.weixin.qq.com/s?t=pages/image_detail&scene=1&__biz=MzkyNzcyMzcxOQ==&mid=2247484485&idx=1&sn=2aeba8624005336483915eab7df5b3d6"
articles[31]="https://mp.weixin.qq.com/s?__biz=Mzg2MTYzNzM5OA==&mid=2247521315&idx=1&sn=88627c2fc11d8371b476e8ea75663b73"
articles[32]="https://mp.weixin.qq.com/s?t=pages/image_detail&scene=1&__biz=MzYyMjg1MDUxMw==&mid=2247485902&idx=1&sn=38947b5df0fd0ada79866b0c895d02c7"
articles[33]="https://mp.weixin.qq.com/s?t=pages/image_detail&scene=1&__biz=MjM5MjU0NzE3MQ==&mid=2247483854&idx=1&sn=769e1c5e542718508a5a91b1d5df54d4"
articles[34]="https://mp.weixin.qq.com/s?__biz=MzIyNDU2NTc5Mw==&mid=2247523289&idx=1&sn=806fc13bce3840caf61aac285adf23c8"
articles[35]="https://mp.weixin.qq.com/s?__biz=MzE5ODQyNDY4OQ==&mid=2247484317&idx=1&sn=dbe55a2dd9186d56f67d16dc7249d0e2"
articles[36]="https://mp.weixin.qq.com/s?t=pages/image_detail&scene=1&__biz=MzYyNTQ1Njk5OA==&mid=2247486313&idx=1&sn=f63b54a0b448ddcf10cf769eef901b8c"
articles[37]="https://mp.weixin.qq.com/s?__biz=MzIwMzA4Njg3Mg==&mid=2650332308&idx=1&sn=f65ed575a7376aaa29b369fd9fd4ae5b"
articles[38]="https://mp.weixin.qq.com/s?__biz=MzIwMzA4Njg3Mg==&mid=2650332581&idx=1&sn=af809ac4a768be2baffb8b097b836b66"
articles[39]="https://mp.weixin.qq.com/s?__biz=MzA4NzgzMjA4MQ==&mid=2453482421&idx=1&sn=7ae5ce79ba54a080ee02c814342763c9"
articles[40]="https://mp.weixin.qq.com/s?__biz=MzIwMzA4Njg3Mg==&mid=2650332333&idx=1&sn=14820525b8dde9e688a35656d3ad464b"
articles[41]="https://mp.weixin.qq.com/s?__biz=MzI2NDU4OTExOQ==&mid=2247695386&idx=1&sn=7b4ec46bedf2b841680912d6be029a81"
articles[42]="https://mp.weixin.qq.com/s?t=pages/image_detail&scene=1&__biz=MzIxMjgxMTY0MQ==&mid=2247484049&idx=1&sn=24cbba6949dab1094821382e91c605b3"
articles[43]="https://mp.weixin.qq.com/s?t=pages/image_detail&scene=1&__biz=MzA3OTIwMDY0MQ==&mid=2247484873&idx=1&sn=c52d750f89df838c1cc7d6e9bba95c74"
articles[44]="https://mp.weixin.qq.com/s?t=pages/image_detail&scene=1&__biz=MzYzMzQzMzIyNw==&mid=2247483681&idx=1&sn=3472db3b721f2dbcd2ec0d3b8454f92d"
articles[45]="https://mp.weixin.qq.com/s?__biz=Mzg2MzgwNzE4Mw==&mid=2247525693&idx=2&sn=88521927e35b47cbae4f911fe5c7f038"
articles[46]="https://mp.weixin.qq.com/s?__biz=MzA4NzgzMjA4MQ==&mid=2453483055&idx=1&sn=aca9f531006d4ae5c50feb6d4cc5229e"
articles[47]="https://mp.weixin.qq.com/s?__biz=MzU4MzQxODEwMg==&mid=2247484371&idx=1&sn=74a047cf91fb0c58e2bdab20fe3cff40"
articles[48]="https://mp.weixin.qq.com/s?__biz=MzA4NzgzMjA4MQ==&mid=2453483050&idx=1&sn=97efd72a35ab30ea62f505b660e96c87"
articles[49]="https://mp.weixin.qq.com/s?__biz=MzA4NzgzMjA4MQ==&mid=2453483005&idx=1&sn=c9f8f61c028246d79060eac3ae9a94e6"
articles[50]="https://mp.weixin.qq.com/s?t=pages/image_detail&scene=1&__biz=MzY5NjE2Njc4NA==&mid=2247484579&idx=1&sn=b2c086aa7612ebc82b10616ce1f4a96c"
articles[51]="https://mp.weixin.qq.com/s?__biz=MzU3MjU5Mzc2Nw==&mid=2247489451&idx=1&sn=ea38ea3d9deb312fea0343e4a240acce"
articles[52]="https://mp.weixin.qq.com/s?__biz=MzA4NzgzMjA4MQ==&mid=2453483153&idx=1&sn=a6310e9a85f60c638e76130639004b80"
articles[53]="https://mp.weixin.qq.com/s?t=pages/image_detail&scene=1&__biz=MzU4Mjg1NzcwNg==&mid=2247484973&idx=1&sn=67ec051c58d3082cdf0f73de42a2da38"
articles[54]="https://mp.weixin.qq.com/s?t=pages/image_detail&scene=1&__biz=MzUyNTg4ODk5Nw==&mid=2247483820&idx=1&sn=2ed984f654b9b07cc619468a5304caae"
articles[55]="https://mp.weixin.qq.com/s?__biz=MzI5ODA4NDg3Mw==&mid=2247483936&idx=1&sn=9e73adaaf0237901b9dc9f8c946750f6"
articles[56]="https://mp.weixin.qq.com/s?t=pages/image_detail&scene=1&__biz=MzU5Njg2ODM4NQ==&mid=2247483963&idx=1&sn=bf72c6ae87af2a85ea62f41469905b70"
articles[57]="https://mp.weixin.qq.com/s?t=pages/image_detail&scene=1&__biz=MzU5NDQ1MjIxNg==&mid=2247492871&idx=1&sn=9337746c1949fd9b76e6f913953481c7"
articles[58]="https://mp.weixin.qq.com/s?__biz=MzY5MTIxNDA0MQ==&mid=2247484184&idx=1&sn=50f938d312b849bf1a0a7d331d90eb08"
articles[59]="https://mp.weixin.qq.com/s?t=pages/image_detail&scene=1&__biz=Mzk5MDYzMDkyMA==&mid=2247485215&idx=1&sn=9855c9c4856e74f4742398cf6410e849"
articles[60]="https://mp.weixin.qq.com/s?t=pages/image_detail&scene=1&__biz=MzYzMTg5ODY4NQ==&mid=2247483869&idx=1&sn=7a916211435a07a3b3ad08450d490af9"
articles[61]="https://mp.weixin.qq.com/s?__biz=MzE5ODQyNDY4OQ==&mid=2247484887&idx=1&sn=b7f86e09a940ec61c40cb4f837df2a25"
articles[62]="https://mp.weixin.qq.com/s?__biz=MzkxNjUxNjg0MA==&mid=2247484174&idx=1&sn=a41da0ecd07949fae20d753fd4b95765"
articles[63]="https://mp.weixin.qq.com/s?__biz=MzkxNjUxNjg0MA==&mid=2247484188&idx=1&sn=b4b1c0e50851cc3f9162278c7c3ecebb"
articles[64]="https://mp.weixin.qq.com/s?__biz=MzY5NzE5MTQ3NA==&mid=2247484124&idx=3&sn=0f8418d5403c1ed27d6784caa55ca958"
articles[65]="https://mp.weixin.qq.com/s?t=pages/image_detail&scene=1&__biz=Mzg3NzEzNzg2Ng==&mid=2247493771&idx=1&sn=0c60d42aaf84f03ba1004e34d9c6f36d"
articles[66]="https://mp.weixin.qq.com/s?t=pages/image_detail&scene=1&__biz=MzUzMDU4MjQ0NA==&mid=2247486325&idx=1&sn=9b87cb5de481c0a7afb39c915d42a3a7"
articles[67]="https://mp.weixin.qq.com/s?__biz=MzI2NDU4OTExOQ==&mid=2247695194&idx=1&sn=030591ea76020210c5f06692fb30243f"
articles[68]="https://mp.weixin.qq.com/s?__biz=MzI2NDU4OTExOQ==&mid=2247695184&idx=1&sn=f48d917721d119b4634ca01619b8bcd8"
articles[69]="https://mp.weixin.qq.com/s?t=pages/image_detail&scene=1&__biz=Mzg3Nzg3MDI2Mw==&mid=2247484473&idx=1&sn=923057f5978adaa55a4da932e7da60c1"

# 清理测试文件
rm -f "$OUTPUT_DIR/test.pdf"

total=${#articles[@]}
success=0
failed=0

echo "=========================================="
echo "开始批量下载 $total 篇微信文章为 PDF"
echo "输出目录: $OUTPUT_DIR"
echo "=========================================="

for i in $(seq 1 $total); do
    url="${articles[$i]}"
    output="$OUTPUT_DIR/$(printf '%02d' $i).pdf"
    
    echo -n "[$i/$total] "
    
    # 使用Chrome headless生成PDF
    "$CHROME" --headless --disable-gpu --no-sandbox \
        --print-to-pdf="$output" \
        --no-pdf-header-footer \
        "$url" 2>/dev/null
    
    if [ -f "$output" ] && [ -s "$output" ]; then
        size=$(ls -lh "$output" | awk '{print $5}')
        echo "✓ 成功 ($size)"
        success=$((success + 1))
    else
        echo "✗ 失败"
        failed=$((failed + 1))
    fi
    
    # 每5个暂停一下
    if [ $((i % 5)) -eq 0 ] && [ $i -lt $total ]; then
        echo "--- 已下载 $i 篇，暂停3秒避免限制 ---"
        sleep 3
    fi
done

echo ""
echo "=========================================="
echo "下载完成！"
echo "成功: $success 篇 | 失败: $failed 篇"
echo "保存位置: $OUTPUT_DIR"
echo "=========================================="
ls -lh "$OUTPUT_DIR" | tail -20
