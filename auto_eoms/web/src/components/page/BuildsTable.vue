<template>

    <div class="builds">
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-lx-cascades"></i> Builds</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-table :data="value" border class="table" ref="multipleTable">
                <el-table-column prop="build_id" label="BuildId" width="320" show-overflow-tooltip></el-table-column>
                <el-table-column prop="build_author" label="BuildAuthor" width="250"
                                 show-overflow-tooltip></el-table-column>
                <el-table-column prop="build_method" label="BuildMethod" width="330"
                                 show-overflow-tooltip></el-table-column>
                <el-table-column label="下载" width="400" show-overflow-tooltip>
                    <template slot-scope="scope">
                        <el-row>
                            <el-button type="text" icon="el-icon-download"  @click="getDebug(scope.row)">debug
                            </el-button>
                            <el-button type="text" icon="el-icon-download"  @click="getIAutoTest(scope.row)">
                                iautotest
                            </el-button>
                            <el-button type="text" icon="el-icon-download"  @click="getItest(scope.row)">itest
                            </el-button>
                            <el-button type="text" icon="el-icon-download"  @click="getRelease(scope.row)">
                                release
                            </el-button>
                        </el-row>
                    </template>

                </el-table-column>
                <el-table-column prop="created_time" label="日期" sortable width="150"
                                 show-overflow-tooltip></el-table-column>
                <el-table-column label="操作" width="160" align="center" show-overflow-tooltip>
                    <template slot-scope="scope">
                        <el-button type="text" icon="el-icon-view" @click="handleView(scope.row)">查看</el-button>
                    </template>
                </el-table-column>
            </el-table>
            <div class="pagination">
                <el-pagination background @current-change="handleCurrentChange" layout="prev, pager, next"
                               :total="total">
                </el-pagination>
            </div>
        </div>


        <!-- 下载弹出框-->
        <el-dialog title="下载"  :visible.sync="editVisible" width="30%">
            <el-table :data="apk_names" border class="table" ref="multipleTable">
                <el-table-column prop="apk_name" min-width="80%" label="包"  show-overflow-tooltip></el-table-column>
                <el-table-column label="操作" min-width="20%" align="center" show-overflow-tooltip>
                    <template slot-scope="scope">
                        <el-button type="text" icon="el-icon-download" @click="downloadApk(scope.row)">下载</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-dialog>
    </div>
</template>

<script>
    import Axios from 'axios'

    export default {
        name: 'BaseTable',
        data() {
            return {
                total: 0,
                value: [],
                commit_id: '',
                apk_path: '',
                editVisible: false,
                apk_names: []
            }
        },
        methods: {
            // 分页导航
            handleCurrentChange(val) {
                this.cur_page = val;
                this.getData();

            },
            handleView(row) {
                this.$router.push({path: '/tests', query: {build_id: row['build_id']}})
            },
            getDebug(row) {
                this.editVisible = true;
                this.apk_path = JSON.parse(JSON.stringify(row['apk_path']))['1'] + 'debug';
                var api ='http://10.1.1.76:9999/api/v1/download?path=' + this.apk_path;
                Axios.get(api, {}).then(res => {
                    this.apk_names = res.data.apk_names;
                }).catch(error => {
                    console.log('Error', error.message)
                })
            },
            getIAutoTest(row) {
                this.editVisible = true;
                this.apk_path = "/";
                var apk_path_list = JSON.parse(JSON.stringify(row['apk_path']))['2'].split('/');
                for (var i = 0; i < apk_path_list.length - 1; i++) {
                    this.apk_path = this.apk_path + "/" + apk_path_list[i]
                }
               var api ='http://10.1.1.76:9999/api/v1/download?path=' + this.apk_path;
                Axios.get(api, {}).then(res => {
                    this.apk_names = res.data.apk_names;
                }).catch(error => {
                    console.log('Error', error.message)
                })
            },
            getItest(row) {
                this.editVisible = true;
                this.apk_path = JSON.parse(JSON.stringify(row['apk_path']))['3'] + 'itest';
                var api ='http://10.1.1.76:9999/api/v1/download?path=' + this.apk_path;
                Axios.get(api, {}).then(res => {
                    this.apk_names = res.data.apk_names;
                }).catch(error => {
                    console.log('Error', error.message)
                })
            },
            getRelease(row) {
                this.editVisible = true;
                this.apk_path = JSON.parse(JSON.stringify(row['apk_path']))['4'] + 'release';
                var api ='http://10.1.1.76:9999/api/v1/download?path=' + this.apk_path;
                Axios.get(api, {}).then(res => {
                    this.apk_names = res.data.apk_names;
                }).catch(error => {
                    console.log('Error', error.message)
                })
            },
            getData() {
                var api = 'http://10.1.1.76:9999/api/v1/commits/builds?commit_id=' + this.commit_id + '&page=' + this.cur_page;
                Axios.get(api, {}).then(res => {
                    this.value = res.data.value;
                }).catch(error => {
                    console.log('Error', error.message)
                })
            },
            downloadApk(row){
                var api = 'http://10.1.1.76:9998/download-apk?apk_name='+ row.apk_name + '&common_path=' + this.apk_path;
                console.log(api);
                location.href = api
            }
        },
        mounted() {
            this.commit_id = this.$route.query.commit_id;
            var api = 'http://10.1.1.76:9999/api/v1/commits/builds?commit_id=' + this.commit_id;
            Axios.get(api, {}).then(res => {
                this.value = res.data.value;
                this.total = res.data.total_num;
            }).catch(error => {
                console.log('Error', error.message)
            });
        },
    }
</script>

<style scoped>
    .el-dropdown-link {
        cursor: pointer;
        color: #409EFF;
    }

    .el-icon-arrow-down {
        font-size: 12px;
    }

    .demonstration {
        display: block;
        color: #8492a6;
        font-size: 14px;
        margin-bottom: 20px;
    }
</style>
