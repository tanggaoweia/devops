<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-download"></i> android phone 手动 build</el-breadcrumb-item>
            </el-breadcrumb>
        </div>

        <div class="container">
            <!--搜索-->
            <div class="handle-box">
                <el-input v-model="select_word" placeholder="搜索" class="handle-input mr10"></el-input>
                <el-button type="primary" icon="el-icon-search" @click="search">搜索</el-button>
                <el-button type="primary" icon="el-icon-delete" @click="empty">清空</el-button>
            </div>
            <!---->

            <!--表格内容-->
            <!--            <el-table :data="value" style="width: 100%">-->
            <el-table :data="value" border class="table" ref="row_table">
                <!--下拉框表格-->
                <el-table-column type="expand">
                    <template slot-scope="scope">
                        <!--                        <el-table :data="value" style="width: 100%">-->
                        <el-table :data="scope.row.data">
                            <el-table-column align="center" fixed label="编号" width="50%">
                                <template slot-scope="scope">
                                    <span>{{scope.$index + 1}}</span>
                                </template>
                            </el-table-column>
                            <el-table-column label="包名" prop="apk_name" width="500px"></el-table-column>
                            <el-table-column label="备注" prop="test_desc" width="300px"></el-table-column>
                            <el-table-column label="是否打标" prop="is_tab" width="100px"></el-table-column>
                            <el-table-column label="是否上传测试报告" prop="is_report" width="150px"></el-table-column>
                            <el-table-column label="测试是否通过" width="250px">
                                <template slot-scope="scope">
                                    <el-select v-model="scope.row.test_result" placeholder="测试是否通过"
                                               @change="handleChange(scope.$index, scope.row)">
                                        <el-option
                                                v-for="item in options"
                                                :key="item.value"
                                                :label="item.label"
                                                :value="item.value">
                                        </el-option>
                                    </el-select>
                                </template>
                            </el-table-column>
                            <el-table-column label="操作" width="500px">
                                <template slot-scope="scope">
                                    <el-button @click="signPreview(scope.$index, scope.row)"
                                               icon="el-icon-view"
                                               type="text">打标
                                    </el-button>
                                    <el-button type="text" icon="el-icon-download"
                                               @click="downloadApk(scope.row)">
                                        下载
                                    </el-button>
                                    <el-button @click="editPreview(scope.$index, scope.row)"
                                               icon="el-icon-edit"
                                               type="text">备注
                                    </el-button>
                                    <el-button @click="cancelSign(scope.$index, scope.row)"
                                               icon="el-icon-delete"
                                               type="text">取消打标
                                    </el-button>
                                    <el-button @click="uploadReport(scope.$index, scope.row)"
                                               icon="el-icon-upload2"
                                               type="text">上传测试报告
                                    </el-button>
                                    <el-button @click="queryReport(scope.$index, scope.row)"
                                               icon="el-icon-upload2"
                                               type="text">删除测试报告
                                    </el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                    </template>
                </el-table-column>
                <!---->
                <el-table-column label="id" prop="pull_request_id" show-overflow-tooltip width="50px"></el-table-column>
                <el-table-column label="build id" prop="build_id" show-overflow-tooltip></el-table-column>
                <el-table-column label="主题" prop="commit_msg" show-overflow-tooltip></el-table-column>
                <el-table-column label="pullRequest完成时间" prop="create_time" show-overflow-tooltip
                                 sortable></el-table-column>
            </el-table>


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

            <!-- 删除测试报告弹出框 -->
            <el-dialog :visible.sync="delReportVisible" title="下载测试报告" width="40%">
                <el-table :data="delReportValue" border class="table" ref="multipleTable">
                    <el-table-column align="center" fixed label="编号" width="50%">
                        <template slot-scope="scope">
                            <span>{{scope.$index + 1}}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="测试报告名称" prop="test_report_name" show-overflow-tooltip
                                     width="500px"></el-table-column>
                    <el-table-column label="操作" show-overflow-tooltip>
                        <template slot-scope="scope">
                            <el-button type="text" icon="el-icon-download" @click="delReport(scope.row)">删除
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </el-dialog>

            <!-- 查看弹出框 -->
            <el-dialog :visible.sync="previewVisible" title="打标" width="50%">
                <el-table :data="signValue" border class="table" ref="multipleTable" @selection-change="changeFun">
                    <el-table-column align="center" fixed label="编号" width="50">
                        <template slot-scope="scope">
                            <span>{{scope.$index + 1}}</span>
                        </template>
                    </el-table-column>
                    <el-table-column type="selection" width="55"></el-table-column>
                    <el-table-column label="过去30天记录" prop="title" show-overflow-tooltip></el-table-column>
                    <el-table-column label="pullRequest完成时间" prop="complete_time" show-overflow-tooltip sortable
                                     width="200%"></el-table-column>
                </el-table>
                <span class="dialog-footer" slot="footer">
                    <el-button @click="sign" type="primary">确 定</el-button>
                </span>
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

            <!-- 取消打标弹出框 -->
            <el-dialog :visible.sync="cancelSignVisible" title="取消打标" width="30%">
                <div class="del-dialog-cnt">取消打标后，市场部将看不到这个包，是否确定取消打标？</div>
                <span class="dialog-footer" slot="footer">
                    <el-button @click="cancelSignVisible = false">取 消</el-button>
                    <el-button @click="cancel" type="primary">确 定</el-button>
                </span>
            </el-dialog>


            <!--上传测试报告-->
            <el-dialog :visible.sync="uploadVisible" title="上传测试报告" width="30%">
                <el-upload
                        :before-upload="beforeUpload"
                        :on-exceed="handleExceed"
                        class="upload-demo"
                        drag
                        ref="upload"
                        action="#"
                        :limit="1"
                        :http-request="uploadFile"
                        multiple>
                    <i class="el-icon-upload"></i>
                    <div class="el-upload__text">将文件拖到此处，或<em>点击选择文件</em></div>
                    <div class="el-upload__tip" slot="tip">只支持上传excel或者word文件，别传错了</div>
                </el-upload>
                <span class="dialog-footer" slot="footer">
                    <el-button @click="uploadVisible = false">取 消</el-button>
                    <el-button style="margin-left: 10px;" size="small" type="success"
                               @click="upload">上传</el-button>
                </span>
            </el-dialog>

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
        name: "APKRelease",
        data() {
            return {
                options: [{
                    value: 0,
                    label: '测试通过'
                }, {
                    value: 1,
                    label: '测试不通过'
                }, {
                    value: 2,
                    label: '未测试'
                }
                ],
                testResult: '未测试',
                textarea: '',
                select_word: '',
                currentPage: 1,
                total: 1,
                editVisible: false,
                downloadVisible: false,
                previewVisible: false,
                cancelSignVisible: false,
                uploadVisible: false,
                delReportVisible: false,
                value: [],
                signValue: [],
                downloadInfo: '',
                editValue: '',
                previewValue: '',
                checkboxValue: '',
                rowValue: [],
                reportFile: '',
                delReportValue: [],
            }
        },
        methods: {

            delReport(row) {
                let id = row.id;
                let apk_id = row.apk_id;
                let api = "/android_phone/del_test_report";
                let params = new URLSearchParams();
                params.append('id', id);
                params.append('apk_id', apk_id);
                axios.post(api, params).then((val) => {
                    let code = val.data.code;
                    let message = val.data.msg;
                    if (code === 1) {
                        this.$message.success(message);
                    } else {
                        this.$message.error(message);
                    }
                });
                this.delReportVisible = false;
            },

            queryReport(index, row) {
                this.delReportVisible = true;
                let apk_id = row.id;
                let api = "/android_phone/market_test_report?id=" + apk_id;
                axios.get(api, {}).then(res => {
                    this.delReportValue = res.data.data;
                }).catch(error => {
                    this.$message.error(error.message)
                })
            },

            beforeUpload(file) {  //判断文件格式
                let hz = file.name.split(".")[1];
                if (hz !== 'xlsx' && hz !== 'xls' && hz !== 'doc' && hz !== 'docx') {
                    this.$message.warning(`请上传xls，xlsx后缀Excel文件或doc, docx后缀的word文档`);
                    return false;
                }
            },

            handleExceed(files, fileList) {   // 上传文件个数超过定义的数量
                this.$message.warning(`当前限制选择 1 个文件，请删除后继续上传`)
            },

            uploadReport(index, row) {
                this.uploadVisible = true;
                this.rowValue = row;
            },

            uploadFile(item) {
                this.reportFile = item.file;
            },

            upload() {
                let api = "/android_phone/test_report";
                let apk_id = this.rowValue.id;
                let params = new FormData();
                params.append("id", apk_id);
                params.append("report", this.reportFile);
                let config = {
                    headers: {"Content-Type": "multipart/form-data"},
                };
                this.$refs.upload.clearFiles();
                axios.post(api, params, config).then((val => {
                    let msg = val.data.msg;
                    let code = val.data.code;
                    if (code === 1) {
                        this.$message.success(msg);
                        this.reportFile = '';
                        this.rowValue.is_report = 1;
                    } else {
                        this.$message.error(msg)
                    }
                })).catch(error => {
                    console.log('Error', error.message)
                });
                this.uploadVisible = false;
            },


            cancel() {
                this.cancelSignVisible = false;
                let api = "/android_phone/cancel_sign";
                let apk_id = this.rowValue.id;
                let params = new URLSearchParams();
                params.append('id', apk_id);
                axios.post(api, params).then((val) => {
                    let code = val.data.code;
                    let message = val.data.msg;
                    if (code === 1) {
                        this.$message.success(message);
                        this.rowValue.is_tab = 0;
                    } else {
                        this.$message.error(message);
                    }
                });
            },

            cancelSign(index, row) {
                this.cancelSignVisible = true;
                this.rowValue = row;
            },

            handleChange(index, row) {
                let obj = {};
                obj = this.options.find((item) => {
                    return item.value === row.test_result; //筛选出匹配数据
                });
                let api = "android_phone/update_test_result";
                let test_result = obj.label;
                let apk_id = row.id;
                let params = new URLSearchParams();
                params.append('id', apk_id);
                params.append('test_result', test_result);
                axios.post(api, params).then((val) => {
                    let code = val.data.code;
                    let message = val.data.msg;
                    if (code === 1) {
                        this.$message.success(message);
                    } else {
                        this.$message.error(message);
                    }
                });

            },

            changeFun(val) {
                this.checkboxValue = val;
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

            signPreview(index, row) {
                this.previewVisible = true;
                this.previewValue = row;
                let time = row.create_time;
                let api = 'android_phone/pull_request_info_of_month?time=' + time;
                axios.get(api, {}).then((val) => {
                    let code = val.data.code;
                    if (code === 1) {
                        this.signValue = val.data.data
                    } else {
                        this.$message.error(message);
                    }
                });
            },

            sign() {
                this.previewVisible = false;
                let sign = [];

                for (let i = 0; i < this.checkboxValue.length; i++) {
                    sign.push(this.checkboxValue[i].pull_request_id)
                }

                let api = 'android_phone/update_sign';
                let apk_id = this.previewValue.id;
                let params = new URLSearchParams();
                params.append('id', apk_id);
                params.append('sign', sign);
                axios.post(api, params).then((val) => {
                    let code = val.data.code;
                    let message = val.data.msg;
                    if (code === 1) {
                        this.$message.success(message);
                        this.previewValue.is_tab = 1;
                    } else {
                        this.$message.error(message);
                    }
                });
            },

            editPreview(index, row) {
                this.textarea = row.test_desc;
                this.editVisible = true;
                this.editValue = row;
            },

            edit() {
                this.editVisible = false;
                let api = 'android_phone/update_description';
                let apk_id = this.editValue.id;
                let description = this.textarea;
                let params = new URLSearchParams();
                params.append('id', apk_id);
                params.append('description', description);
                axios.post(api, params).then((val) => {
                    let code = val.data.code;
                    let message = val.data.msg;
                    if (code === 1) {
                        this.$message.success(message);
                        this.editValue.test_desc = this.textarea;
                    } else {
                        this.$message.error(message);
                    }
                });
            },

            search() {
                this.currentPage = 1;
                if (this.select_word !== '') {
                    let api = "/android_phone/table_info_where_pull_request_id_is_zero?page_num=1&select_word=" + this.select_word;
                    axios.get(api, {}).then(res => {
                        this.value = res.data.data;
                        this.total = res.data.total;
                    }).catch(error => {
                        this.$message.error(error.message)
                    })
                } else {
                    this.getData(1);
                }
            },

            empty() {
                if (this.select_word !== '') {
                    this.select_word = '';
                    this.getData(1);
                    this.currentPage = 1;
                }
            },

            handleSizeChange(val) {
                console.log(`每页 ${val} 条`);
            },

            handleCurrentChange(val) {
                this.getData(val);
            },

            getData(page_num) {
                let api = "/android_phone/table_info_where_pull_request_id_is_zero?page_num=" + page_num;
                if (this.select_word !== '') {
                    api = "/android_phone/table_info_where_pull_request_id_is_zero?page_num=" + page_num + "&select_word=" + this.select_word;
                }
                axios.get(api, {}).then(res => {
                    this.value = res.data.data;
                    this.total = res.data.total;
                }).catch(error => {
                    this.$message.error(error.message)
                })
            }
        }
        ,

        created() {
            this.getData(1);
        }
    }
</script>

<style scoped>

    .el-table .warning-row {
        background: oldlace;
    }

    .el-table .success-row {
        background: #f0f9eb;
    }

    .demo-table-expand {
        font-size: 0;
    }

    .demo-table-expand label {
        width: 90px;
        color: #99a9bf;
    }

    .demo-table-expand .el-form-item {
        margin-right: 0;
        margin-bottom: 0;
        width: 50%;
    }

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