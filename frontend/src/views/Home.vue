<script setup>
import { ref, onMounted } from "vue";
import client from '../api/client';

const tags = ref([]);

onMounted(async () => {
    const response = await client.get('/tags');
    console.log(response);
    tags.value = response.data
})
</script>

<template>
    <h1>ホーム画面</h1>
    <ul>
        <li v-for="tag in tags" :key="tag.tag_id">{{ tag.title }}</li> 
    </ul>
</template>