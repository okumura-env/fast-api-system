<template>
    <div class="app">
        <header class="header">
            <span class="header-title">Recipe Manager</span>
        </header>
        <div class="container">
            <nav class="sidebar">
                <router-link to="/">ホーム</router-link>
                <router-link to="/recipes">レシピ一覧</router-link>
                <router-link to="/ingredients">食材一覧</router-link>
                <router-link to="/tags">タグ一覧</router-link>
                <router-link to="/users">ユーザー一覧</router-link>
            </nav>
            <main class="content">
                <router-view />
            </main>
        </div>
    </div>
</template>
