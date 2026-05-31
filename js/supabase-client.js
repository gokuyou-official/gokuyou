(function () {
  try {
    var URL = window.GOKUYOU_CONFIG.SUPABASE_URL;
    var KEY = window.GOKUYOU_CONFIG.SUPABASE_KEY;

    window.supabaseClient = supabase.createClient(URL, KEY, {
      auth: {
        persistSession: true,
        autoRefreshToken: true,
        detectSessionInUrl: true,
        flowType: 'implicit',
        storageKey: 'gokuyou-auth'
      }
    });

    window.gAuth = {
      signIn: function (email) {
        return window.supabaseClient.auth.signInWithOtp({
          email: email,
          options: {
            emailRedirectTo: 'https://gokuyou-official.github.io/gokuyou/pages/auth-callback.html'
          }
        });
      },
      signOut: async function () {
        try {
          await window.supabaseClient.auth.signOut();
        } catch (e) {
          console.error(e);
        }
        window.location.href = '/gokuyou/pages/login.html';
      },
      getSession: async function () {
        var result = await window.supabaseClient.auth.getSession();
        return result.data.session;
      }
    };

    // セッション変化を監視してトークン自動更新
    window.supabaseClient.auth.onAuthStateChange(function (event, session) {
      if (event === 'SIGNED_OUT') {
        var currentPath = window.location.pathname;
        var protectedPaths = ['/gokuyou/pages/profile.html'];
        if (protectedPaths.indexOf(currentPath) !== -1) {
          window.location.href = '/gokuyou/pages/login.html';
        }
      }
    });

    document.addEventListener('DOMContentLoaded', function () {
      try {
        window.supabaseClient.auth.getSession().then(function (result) {
          var session = result && result.data ? result.data.session : null;

          // サイドバーのナビリンク（navLinkは<a>要素のため入れ子にならないよう直接設定）
          var navLink = document.getElementById('nav-auth-link');
          if (navLink) {
            if (session) {
              navLink.href = '/gokuyou/pages/profile.html';
              navLink.textContent = 'マイページ';
            } else {
              navLink.href = '/gokuyou/pages/login.html';
              navLink.textContent = 'ログイン';
            }
          }

          // ヒーローセクションの認証リンク（index.html）
          var heroLink = document.getElementById('hero-auth-link');
          if (heroLink) {
            if (session) {
              heroLink.href = '/gokuyou/pages/profile.html';
              heroLink.textContent = '👤 マイページ';
            } else {
              heroLink.href = '/gokuyou/pages/login.html';
              heroLink.textContent = '👤 ログイン / マイページ';
            }
          }
        }).catch(function (e) {
          console.error(e);
        });
      } catch (e) {
        console.error(e);
      }
    });
  } catch (e) {
    console.error(e);
  }
})();
