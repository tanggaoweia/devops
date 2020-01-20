<template>
    <div class="help">
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-help"></i> 帮助</el-breadcrumb-item>
            </el-breadcrumb>
        </div>

        <div class="container">
            <p class="handle-box ">
                <el-tag type="info">所有测试文档地址：\\10.1.1.63\Development\汤高伟的测试文档</el-tag>

            </p>
            <p class="handle-box">
                <el-tag type="info">运维平台操作文档文件名：运维平台操作文档.docx</el-tag>

            </p>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Help"
    }
</script>

<style scoped>
    .handle-box {
        margin-bottom: 20px;
    }

    .handle-select {
        width: 120px;
    }

    .handle-input {
        width: 300px;
        display: inline-block;
    }

    .table {
        width: 100%;
        font-size: 14px;
    }

    .mr10 {
        margin-right: 10px;
    }

</style>