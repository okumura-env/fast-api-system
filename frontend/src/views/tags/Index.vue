<script setup>
import { ref, onMounted } from "vue";
import client from '../../api/client';

const tags = ref([]);

const editTag = (id) => {
    console.log(id + " 編集")
}

const deleteTag = (id) => {
    console.log(id + " 削除成功")
}

onMounted(async () => {
    const response = await client.get('/tags');
    console.log(response);
    tags.value = response.data
})
</script>

<template>
    <div class="page-header">
        <h1>タグ一覧</h1>
        <router-link to="/tags/create" class="btn-submit">新規登録</router-link>
    </div>

    <!-- タグ一覧 -->
    <table class="tag-table">
        <thead>
            <tr>
                <th>ID</th>
                <th>タグ名</th>
                <th>操作</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="tag in tags" :key="tag.tag_id">
                <td>{{ tag.tag_id }}</td>
                <td>{{ tag.title }}</td>
                <td class="tag-actions">
                    <button class="btn-edit" @click="editTag(tag.tag_id)">編集</button>
                    <button class="btn-delete" @click="deleteTag(tag.tag_id)">削除</button>
                </td>
            </tr>
        </tbody>
    </table>
</template>