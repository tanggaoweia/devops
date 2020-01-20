<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-video-camera"></i> 模型和网络</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">

            <!--搜索和模型网络上传-->
            <div class="handle-box">
                <el-input v-model="select_word" placeholder="搜索" class="handle-input mr10"></el-input>
                <el-button type="primary" icon="el-icon-search" @click="search">搜索</el-button>
                <el-button type="primary" icon="el-icon-delete" @click="empty">清空</el-button>
                <el-button type="primary" icon="el-icon-check" @click="uploadFrame">上传</el-button>
            </div>
            <!---->

            <!--表格信息显示 -->
            <el-table :data="value" border class="table" ref="multipleTable">
                <el-table-column align="center" fixed label="编号" width="40%">
                    <template slot-scope="scope">
                        <span>{{scope.$index + 1}}</span>
                    </template>
                </el-table-column>
                <el-table-column label="模型名称" prop="models_name" show-overflow-tooltip></el-table-column>
                <el-table-column label="模型大小(b)" prop="models_size" show-overflow-tooltip></el-table-column>
                <el-table-column label="flops" prop="flops" show-overflow-tooltip></el-table-column>
                <el-table-column label="total params" prop="total_params" show-overflow-tooltip></el-table-column>
                <el-table-column label="flops脚本状态" prop="flops_result" show-overflow-tooltip></el-table-column>
                <el-table-column label="时间" prop="create_time" show-overflow-tooltip sortable
                                 width="200px"></el-table-column>
                <el-table-column label="操作" show-overflow-tooltip width="300px">
                    <template slot-scope="scope">
                        <el-button @click="handlePreview(scope.$index, scope.row)" icon="el-icon-view" type="text">查看
                        </el-button>
                        <el-button type="text" icon="el-icon-download" @click="downloadModels(scope.row)">模型下载
                        </el-button>
                        <el-button type="text" icon="el-icon-download" @click="downloadNetwork(scope.row)">网络下载
                        </el-button>
                        <el-button type="text" icon="el-icon-s-claim" @click="runScript(scope.row)">执行脚本</el-button>
                    </template>
                </el-table-column>
            </el-table>
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

            <!--模型和网络上传弹出框-->
            <el-dialog :visible.sync="uploadVisible" title="模型和网络上传" width="30%">
                <el-upload
                        class="upload-demo"
                        drag
                        ref="upload"
                        action="#"
                        :http-request="uploadFile"
                        multiple>
                    <i class="el-icon-upload"></i>
                    <div class="el-upload__text">将文件拖到此处，或<em>点击选择文件</em></div>
                    <div class="el-upload__tip" slot="tip">选择网络和模型后，点击右下角上传</div>
                </el-upload>
                <span class="dialog-footer" slot="footer">
                    <el-button @click="uploadVisible = false">取 消</el-button>
                    <el-button style="margin-left: 10px;" size="small" type="success"
                               @click="upload">上传</el-button>
                </span>
            </el-dialog>
            <!---->

            <!--查看弹框-->
            <el-dialog :visible.sync="previewVisible" title="网络模型flops" width="60%">
                <el-table :data="rowValue" border class="table" ref="multipleTable">
                    <el-table-column align="center" fixed label="编号" width="40%">
                        <template slot-scope="scope">
                            <span>{{scope.$index + 1}}</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="flops" prop="flops" show-overflow-tooltip></el-table-column>
                    <el-table-column label="kernel_size" prop="kernel_size" show-overflow-tooltip></el-table-column>
                    <el-table-column label="layers_name" prop="layers_name" show-overflow-tooltip></el-table-column>
                    <el-table-column label="output_shape" prop="output_shape" show-overflow-tooltip></el-table-column>
                    <el-table-column label="param" prop="param" show-overflow-tooltip></el-table-column>
                </el-table>
            </el-dialog>
            <!---->

            <!--模型下载弹出框-->
            <el-dialog :visible.sync="modelDownLoadVisible" title="模型下载" width="30%">
                <div class="del-dialog-cnt">下载需要一定的时间，是否确定下载？</div>
                <span class="dialog-footer" slot="footer">
                    <el-button @click="modelDownLoadVisible = false">取 消</el-button>
                    <el-button @click="downloadModelsActive" type="primary">确 定</el-button>
                </span>
            </el-dialog>
            <!---->


            <!--网络下载弹出框-->
            <el-dialog :visible.sync="networkDownLoadVisible" title="网络下载" width="30%">
                <div class="del-dialog-cnt">下载需要一定的时间，是否确定下载？</div>
                <span class="dialog-footer" slot="footer">
                    <el-button @click="networkDownLoadVisible = false">取 消</el-button>
                    <el-button @click="downloadNetworkActive" type="primary">确 定</el-button>
                </span>
            </el-dialog>
            <!---->

            <!--执行flops脚本弹出框-->
            <el-dialog :visible.sync="runFlopsScriptVisible" title="执行flops脚本" width="30%">
                <div class="del-dialog-cnt">是否确定执行flops脚本？</div>
                <span class="dialog-footer" slot="footer">
                    <el-button @click="runFlopsScriptVisible = false">取 消</el-button>
                    <el-button @click="runFlopsScript" type="primary">确 定</el-button>
                </span>
            </el-dialog>
            <!---->

        </div>
    </div>
</template>

<script>
    import Axios from 'axios'

    export default {
        name: "ModelsAndNetworks",
        data() {
            return {
                select_word: '',
                uploadVisible: false,
                previewVisible: false,
                modelDownLoadVisible: false,
                networkDownLoadVisible: false,
                runFlopsScriptVisible: false,
                modelsFile: '',
                modelName: '',
                prototxtFile: '',
                prototxtName: '',
                value: [],
                currentPage: 0,
                total: 1,
                rowValue: [],
                baseUrl: "http://10.1.1.111:8888",
            }
        },
        methods: {

            runScript(row) {
                this.runFlopsScriptVisible = true;
                this.rowValue = row;
            },

            runFlopsScript() {
                this.runFlopsScriptVisible = false;
                let api = this.baseUrl + "/dl_model_manager/flops_script_sign";
                let params = new URLSearchParams();
                params.append('id', this.rowValue.id);
                Axios.post(api, params).then((val) => {
                    let code = val.data.code;
                    let message = val.data.msg;
                    if (code === 1) {
                        let api = this.baseUrl + "/dl_model_manager/full_info?page_num=1";
                        this.getData(api);
                        this.$message.success(message);
                    } else {
                        this.$message.error(message);
                    }
                });
            },

            downloadModelsActive() {
                this.modelDownLoadVisible = false;
                let modelsPath = this.rowValue.models_path;
                this.download(modelsPath);
            },

            downloadNetworkActive() {
                this.networkDownLoadVisible = false;
                let networksPath = this.rowValue.networks_path;
                this.download(networksPath);
            },

            download(path) {
                let api = this.baseUrl + "/download_apk?apk_location=" + path;
                window.open(api);
            },

            downloadModels(row) {
                this.modelDownLoadVisible = true;
                this.rowValue = row;
            },

            downloadNetwork(row) {
                this.networkDownLoadVisible = true;
                this.rowValue = row;
            },

            search() {
                let api = this.baseUrl + "/dl_model_manager/full_info?page_num=1&select_word=" + this.select_word;
                if (this.select_word === "") {
                    api = this.baseUrl + "/dl_model_manager/full_info?page_num=1";
                }
                this.getData(api);
            },

            empty() {
                this.select_word = "";
                let api = this.baseUrl + "/dl_model_manager/full_info?page_num=1";
                this.getData(api);
            },

            uploadFrame() {
                this.uploadVisible = true;
            },

            upload() {
                let api = this.baseUrl + '/dl_model_manager/models_and_networks_upload';
                let params = new FormData();
                params.append(this.modelName, this.modelsFile);
                params.append(this.prototxtName, this.prototxtFile);
                let config = {
                    headers: {"Content-Type": "multipart/form-data"},
                };
                this.$refs.upload.clearFiles();
                Axios.post(api, params, config).then((val => {
                    let msg = val.data.msg;
                    let code = val.data.code;
                    if (code === 1) {
                        this.$message.success(msg);
                        this.modelName = '';
                        this.modelsFile = '';
                        this.prototxtName = '';
                        this.prototxtFile = '';
                        let api = this.baseUrl + "/dl_model_manager/full_info?page_num=1";
                        this.getData(api);
                    } else {
                        this.$message.error(msg)
                    }
                })).catch(error => {
                    console.log('Error', error.message)
                });
                this.uploadVisible = false;
            },

            uploadFile(item) {
                let file = item.file.name.split('.');
                let fileType = file[1];
                if (fileType === 'prototxt') {
                    this.prototxtFile = item.file;
                    this.prototxtName = item.file.name
                } else {
                    this.modelsFile = item.file;
                    this.modelName = item.file.name;
                }
            },

            handlePreview(index, row) {
                this.previewVisible = true;
                this.rowValue = [];
                let flopsData = row.flops_result_info;
                if (flopsData !== "") {
                    this.rowValue = flopsData.data;
                }
            },

            handleSizeChange(val) {
                console.log(`每页 ${val} 条`);
            },

            handleCurrentChange(val) {
                let api = this.baseUrl + "/dl_model_manager/full_info?page_num=" + val + "&select_word=" + this.select_word;
                if (this.select_word === "") {
                    api = this.baseUrl + "/dl_model_manager/full_info?page_num=" + val;
                }
                this.getData(api);
            },

            getData(api) {
                Axios.get(api, {}).then(res => {
                    this.value = res.data.data;
                    this.total = res.data.total;
                }).catch(error => {
                    this.$message.error(error.message)
                })
            }
        },
        created() {
            let api = this.baseUrl + "/dl_model_manager/full_info?page_num=1";
            this.getData(api);
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