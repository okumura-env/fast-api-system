<script setup>
import { ref, onMounted } from "vue";
import client from '../../api/client';
import { useRouter } from "vue-router";

const router = useRouter();
const tags = ref([]);

const goToEdit = (id) => {
        router.push({ name: "tags-edit", params: { id: id } });
    };

const deleteTag = async(tag_id) => {
    await client.delete(`/tags/${tag_id}`);

    tags.value = tags.value.filter(t => t.id !== tag_id)
}

const fetchTags = async() => {
    const response = await client.get('/tags');
    tags.value = response.data
}

onMounted(() => {
    fetchTags();
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
            <tr v-for="tag in tags" :key="tag.id">
                <td>{{ tag.id }}</td>
                <td>{{ tag.title }}</td>
                <td class="tag-actions">
                    <button class="btn-edit" @click="goToEdit(tag.id)">編集</button>
                    <button class="btn-delete" @click="deleteTag(tag.id)">削除</button>
                </td>
            </tr>
        </tbody>
    </table>
</template>