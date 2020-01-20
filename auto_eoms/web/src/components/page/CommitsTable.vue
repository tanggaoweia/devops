<template>
    <div class="commits">
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item><i class="el-icon-lx-cascades"></i> Commits</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">

           <div class="handle-box">
                <el-input v-model="select_word" placeholder="commitId or commitAuthor" class="handle-input mr10"></el-input>
                <el-button type="primary" icon="el-icon-search" @click="search" >搜索</el-button>
                <el-button type="primary" icon="el-icon-delete" @click="empty" >清空</el-button>
            </div>

            <el-table :data="value" border class="table" ref="multipleTable">
                <el-table-column prop="commit_id" label="CommitId" width="350" show-overflow-tooltip></el-table-column>
                <el-table-column prop="commit_msg" label="CommitMsg" width="320" show-overflow-tooltip></el-table-column>
                <el-table-column prop="commit_author" label="CommitAuthor" width="250" show-overflow-tooltip></el-table-column>
                <el-table-column prop="linked_work_item" label="LinkedWorkItem"  show-overflow-tooltip></el-table-column>
                <el-table-column prop="branch" label="Branch" width="100" show-overflow-tooltip></el-table-column>
                <el-table-column prop="created_time" label="日期" sortable width="200" show-overflow-tooltip></el-table-column>
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
                select_word: '',
            }
        },
        methods: {
            // 分页导航
            handleCurrentChange(val) {
                this.cur_page = val;
                this.getData();

            },
            handleView(row) {
                this.$router.push({path:'/builds', query:{commit_id: row['commit_id']}})
            },
            getData() {
                var api = 'http://10.1.1.76:9999/api/v1/commits?page='+ this.cur_page;
                if( this.select_word != ""){
                   api = 'http://10.1.1.76:9999/api/v1/query?select_info=' + this.select_word + '&page='+ this.cur_page;
                }
                Axios.get(api, {}).then(res => {
                    this.value = res.data.value;
                }).catch(error => {
                    console.log('Error', error.message)
                })
            },
            search(){
                var api = 'http://10.1.1.76:9999/api/v1/query?select_info=' + this.select_word;
                if( this.select_word == ""){
                    api = 'http://10.1.1.76:9999/api/v1/commits';
                }
                Axios.get(api, {}).then(res => {
                    this.value = res.data.value;
                    this.total = res.data.total_num;
                }).catch(error => {
                    console.log('Error', error.message)
                })
            },
            empty(){
                this.select_word = ''
            }
        },
        created() {
            var api = 'http://10.1.1.76:9999/api/v1/commits';
                Axios.get(api, {}).then(res => {
                    this.value = res.data.value;
                    this.total = res.data.total_num;
                }).catch(error => {
                    console.log('Error', error.message)
                })
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
    .table{
        width: 100%;
        font-size: 14px;
    }
    .mr10{
        margin-right: 10px;
    }

</style>
