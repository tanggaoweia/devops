<template>

    <div class="download">
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-download"></i> android phone下载</el-breadcrumb-item>
            </el-breadcrumb>
        </div>

        <div class="container">
            <!--搜索-->
            <div class="handle-box">
                <el-input v-model="select_word" placeholder="搜索" class="handle-input mr10"></el-input>
                <el-date-picker class="handle-input mr10"
                                v-model="startData"
                                type="date"
                                value-format="yyyy-MM-dd"
                                placeholder="开始时间">
                </el-date-picker>

                <el-date-picker class="handle-input mr10"
                                v-model="endData"
                                value-format="yyyy-MM-dd"
                                type="date"
                                placeholder="结束时间">
                </el-date-picker>
                <el-button type="primary" icon="el-icon-search" @click="search">搜索</el-button>
                <el-button type="primary" icon="el-icon-delete" @click="empty">清空</el-button>
            </div>

            <!---->

            <!--     表格信息显示       -->
            <el-table :data="value" border class="table" ref="multipleTable">
                <el-table-column align="center" fixed label="编号" width="50%">
                    <template slot-scope="scope">
                        <span>{{scope.$index + 1}}</span>
                    </template>
                </el-table-column>
                <el-table-column label="时间" prop="update_time" show-overflow-tooltip sortable
                                 width="200px"></el-table-column>
                <el-table-column label="包名" prop="apk_name" show-overflow-tooltip width="500px"></el-table-column>
                <el-table-column label="目标客户" prop="branch" show-overflow-tooltip></el-table-column>
                <el-table-column label="测试员备注" prop="test_desc" show-overflow-tooltip></el-table-column>
                <el-table-column label="备注" prop="market_desc" show-overflow-tooltip></el-table-column>
                <el-table-column label="操作" show-overflow-tooltip width="300px">
                    <template slot-scope="scope">
                        <el-button @click="handlePreview(scope.$index, scope.row)" icon="el-icon-view" type="text">查看
                        </el-button>
                        <el-button type="text" icon="el-icon-download" @click="downloadApk(scope.row)">下载包</el-button>
                        <el-button type="text" icon="el-icon-edit" @click="handleEdit(scope.row)">备注
                        </el-button>
                        <el-button type="text" icon="el-icon-download" @click="downloadReport(scope.row)">下载测试报告
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
            <!--            -->

            <!-- 查看弹出框 -->
            <el-dialog :visible.sync="previewVisible" title="查看" width="30%">
                <el-table :data="previewValue" border class="table" ref="multipleTable">
                    <el-table-column align="center" fixed label="编号" width="50">
                        <template slot-scope="scope">
                            <span>{{scope.$index + 1}}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="主题" prop="title" show-overflow-tooltip></el-table-column>
                    <el-table-column label="pullRequest完成时间" prop="complete_time" show-overflow-tooltip
                                     sortable></el-table-column>
                </el-table>
            </el-dialog>
            <!---->

            <!-- 下载包弹出提示框 -->
            <el-dialog :visible.sync="downloadVisible" title="下载" width="30%">
                <div class="del-dialog-cnt">下载需要一定的时间，是否确定下载？</div>
                <span class="dialog-footer" slot="footer">
                    <el-button @click="downloadVisible = false">取 消</el-button>
                    <el-button @click="download" type="primary">确 定</el-button>
                </span>
            </el-dialog>

            <!-- 下载测试报告弹出框 -->
            <el-dialog :visible.sync="downloadReportVisible" title="下载测试报告" width="40%">
                <el-table :data="reportValue" border class="table" ref="multipleTable">
                    <el-table-column align="center" fixed label="编号" width="50%">
                        <template slot-scope="scope">
                            <span>{{scope.$index + 1}}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="测试报告名称" prop="test_report_name" show-overflow-tooltip width="500px"></el-table-column>
                    <el-table-column label="操作" show-overflow-tooltip >
                        <template slot-scope="scope">
                            <el-button type="text" icon="el-icon-download" @click="downloadTestReport(scope.row)">下载
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </el-dialog>

            <!-- 备注弹出框 -->
            <el-dialog :visible.sync="editVisible" title="备注" width="50%">
                <el-input
                        type="textarea"
                        placeholder="请输入内容"
                        v-model="textarea"
                        :autosize="{ minRows: 1, maxRows: 10}"
                        maxlength="2500"
                        show-word-limit
                >
                </el-input>
                <span class="dialog-footer" slot="footer">
                    <el-button @click="edit" type="primary">确 定</el-button>
                </span>
            </el-dialog>
            <!---->

            <!--分页-->
            <div class="pagination">
                <el-pagination
                        :current-page.sync="currentPage"
                        :page-size="10"
                        :total=total
                        @current-change="handleCurrentChange"
                        @size-change="handleSizeChange"
                        layout="prev, pager, next, jumper">
                </el-pagination>
            </div>
            <!---->
        </div>
    </div>
</template>

<script>
    export default {
        name: "Download",
        data() {
            return {
                select_word: '',
                downloadVisible: false,
                previewVisible: false,
                delVisible: false,
                editVisible: false,
                downloadReportVisible: false,
                startData: '',
                endData: '',
                total: 1,
                currentPage: 1,
                value: [],
                previewValue: [],
                downloadInfo: '',
                rowValue: '',
                textarea: '',
                editValue: '',
                reportValue: [],
            }
        },
        methods: {

            handleEdit(row) {
                this.editVisible = true;
                this.editValue = row;
                this.textarea = this.editValue.market_desc;
            },

            edit() {
                this.editVisible = false;
                let api = "/android_phone/update_market_desc";
                let apk_id = this.editValue.id;
                let params = new URLSearchParams();
                params.append('id', apk_id);
                params.append('description', this.textarea);
                axios.post(api, params).then((val) => {
                    let code = val.data.code;
                    let message = val.data.msg;
                    if (code === 1) {
                        let api = "android_phone/market_table_info?page_num=" + this.currentPage;
                        this.getData(api);
                        this.editValue.market_desc = this.textarea;
                        this.$message.success(message);
                    } else {
                        this.$message.error(message);
                    }
                });
            },

            downloadTestReport(row){
                 this.downloadReportVisible = false;
                let report_id = row.id;
                let api = axios.defaults.baseURL + "/android_phone/download_test_report?id=" + report_id;
                window.open(api)
            },

            downloadReport(row) {
                this.downloadReportVisible = true;
                let apk_id = row.id;
                let api = "/android_phone/market_test_report?id=" + apk_id;
                axios.get(api, {}).then(res => {
                    this.reportValue = res.data.data;
                }).catch(error => {
                    this.$message.error(error.message)
                })
            },

            download() {
                this.downloadVisible = false;
                let api = axios.defaults.baseURL + "/download_apk?apk_location=" + this.downloadInfo.apk_location;
                window.open(api);
            },

            downloadApk(row) {
                this.downloadVisible = true;
                this.downloadInfo = row;
            },

            handlePreview(index, row) {
                this.previewVisible = true;
                let apk_id = row.id;
                let api = "/android_phone/sign_pull_request_info?id=" + apk_id;
                axios.get(api, {}).then(res => {
                    this.previewValue = res.data.data;
                }).catch(error => {
                    this.$message.error(error.message)
                })
            },

            search() {
                let api = "android_phone/market_table_info?page_num=" + this.currentPage + "&select_word=" + this.select_word
                    + "&start_time=" + this.startData + "&end_time=" + this.endData;
                if (this.select_word !== '' || this.startData !== '' || this.endData !== '') {
                    this.getData(api)
                }
            },

            empty() {
                this.currentPage = 1;
                this.select_word = '';
                this.startData = '';
                this.endData = '';
                let api = "android_phone/market_table_info?page_num=1";
                this.getData(api)
            },

            handleSizeChange(val) {
                console.log(`每页 ${val} 条`);
            },

            handleCurrentChange(val) {

                let api = "android_phone/market_table_info?page_num=" + val;
                if (this.select_word !== '' || this.startData !== '' || this.endData !== '') {
                    api = "android_phone/market_table_info?page_num=" + val + "&select_word=" + this.select_word
                        + "&start_time=" + this.startData + "&end_time=" + this.endData;
                }
                this.getData(api)
            },

            getData(api) {
                axios.get(api, {}).then(res => {
                    this.value = res.data.data;
                    this.total = res.data.total;
                }).catch(error => {
                    this.$message.error(error.message)
                })
            }
        },
        created() {
            let api = "android_phone/market_table_info?page_num=1";
            this.getData(api)
        }
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