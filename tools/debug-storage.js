/**
 * 프론트엔드 LocalStorage 디버그 도구
 * 
 * 브라우저 콘솔에서 실행하여 저장소 상태를 확인합니다.
 * 
 * 사용법:
 *   1. 브라우저에서 F12 (개발자 도구) 열기
 *   2. Console 탭 선택
 *   3. 이 파일의 내용을 복사/붙여넣기
 *   4. 또는: window.__storageDebug 객체 사용 (이미 내장됨)
 */

const StorageDebug = {
  // ============================================================
  // 1. 전체 스토리지 조회
  // ============================================================
  
  viewAll: function() {
    console.log('📦 LocalStorage 전체 조회\n');
    
    const result = {};
    const keys = [];
    
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      keys.push(key);
      
      try {
        const raw = localStorage.getItem(key);
        result[key] = JSON.parse(raw);
      } catch (e) {
        result[key] = localStorage.getItem(key);
      }
    }
    
    console.table(keys.map(k => ({
      key: k,
      size: (localStorage.getItem(k) || '').length * 2 + ' bytes',
      type: typeof result[k]
    })));
    
    return result;
  },
  
  // ============================================================
  // 2. 포트폴리오 상세 조회
  // ============================================================
  
  viewPortfolio: function() {
    console.log('📊 포트폴리오 조회\n');
    
    const KEYS = {
      new: 'sp-portfolio-v1',
      legacy: 'stock-predictor-portfolio'
    };
    
    for (const [name, key] of Object.entries(KEYS)) {
      const raw = localStorage.getItem(key);
      
      if (!raw) {
        console.log(`❌ ${name} (${key}): 없음`);
        continue;
      }
      
      try {
        const data = JSON.parse(raw);
        console.log(`✅ ${name} (${key}):`);
        
        // 신버전 형식 (v 필드 있음)
        if (data.v) {
          console.log('   📦 신버전 형식 (압축됨)');
          console.log('   버전:', data.v);
          console.log('   체크섬:', data.c);
          console.log('   저장 시각:', new Date(data.t).toLocaleString());
          console.log('   데이터:', data.d);
          
          // items 확인
          const items = data.d?.i || data.d?.items || [];
          console.log(`   종목 수: ${items.length}개`);
          
          if (items.length > 0) {
            console.table(items.map(i => ({
              ticker: i.t || i.ticker,
              name: i.n || i.name,
              quantity: i.q || i.quantity,
              buyPrice: i.bp || i.buyPrice,
              currentPrice: i.cp || i.currentPrice
            })));
          }
        } else {
          // 구버전 형식
          console.log('   📦 구버전 형식 (비압축)');
          console.log('   데이터:', data);
          
          if (data.items) {
            console.log(`   종목 수: ${data.items.length}개`);
            console.table(data.items);
          }
        }
      } catch (e) {
        console.error(`❌ ${name} (${key}): 파싱 실패`, e);
        console.log('   Raw:', raw.substring(0, 200) + '...');
      }
      
      console.log('');
    }
  },
  
  // ============================================================
  // 3. 즐겨찾기 조회
  // ============================================================
  
  viewFavorites: function() {
    console.log('⭐ 즐겨찾기 조회\n');
    
    const KEYS = {
      new: 'sp-favorites-v1',
      legacy: 'stock-predictor-favorites'
    };
    
    for (const [name, key] of Object.entries(KEYS)) {
      const raw = localStorage.getItem(key);
      
      if (!raw) {
        console.log(`❌ ${name} (${key}): 없음`);
        continue;
      }
      
      try {
        const data = JSON.parse(raw);
        console.log(`✅ ${name} (${key}):`, data);
      } catch (e) {
        console.error(`❌ ${name} (${key}): 파싱 실패`, e);
      }
    }
  },
  
  // ============================================================
  // 4. 알림 조회
  // ============================================================
  
  viewAlerts: function() {
    console.log('🔔 알림 조회\n');
    
    const KEYS = {
      new: 'sp-alerts-v1',
      legacy: 'stock-predictor-alerts'
    };
    
    for (const [name, key] of Object.entries(KEYS)) {
      const raw = localStorage.getItem(key);
      
      if (!raw) {
        console.log(`❌ ${name} (${key}): 없음`);
        continue;
      }
      
      try {
        const data = JSON.parse(raw);
        console.log(`✅ ${name} (${key}):`, data);
      } catch (e) {
        console.error(`❌ ${name} (${key}): 파싱 실패`, e);
      }
    }
  },
  
  // ============================================================
  // 5. 백테스트 히스토리 조회
  // ============================================================
  
  viewBacktest: function() {
    console.log('📈 백테스트 히스토리 조회\n');
    
    const KEYS = {
      new: 'sp-backtest-v1',
      legacy: 'stock-predictor-backtest-history'
    };
    
    for (const [name, key] of Object.entries(KEYS)) {
      const raw = localStorage.getItem(key);
      
      if (!raw) {
        console.log(`❌ ${name} (${key}): 없음`);
        continue;
      }
      
      try {
        const data = JSON.parse(raw);
        console.log(`✅ ${name} (${key}):`, data);
      } catch (e) {
        console.error(`❌ ${name} (${key}): 파싱 실패`, e);
      }
    }
  },
  
  // ============================================================
  // 6. 스토리지 사용량
  // ============================================================
  
  getUsage: function() {
    console.log('📊 스토리지 사용량\n');
    
    let totalBytes = 0;
    const items = [];
    
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      const value = localStorage.getItem(key) || '';
      const bytes = (key.length + value.length) * 2; // UTF-16
      
      totalBytes += bytes;
      items.push({
        key,
        size: bytes,
        sizeKB: (bytes / 1024).toFixed(2) + ' KB'
      });
    }
    
    items.sort((a, b) => b.size - a.size);
    
    console.table(items);
    console.log(`\n총 사용량: ${(totalBytes / 1024).toFixed(2)} KB / 5,120 KB (5 MB 제한)`);
    console.log(`사용률: ${(totalBytes / (5 * 1024 * 1024) * 100).toFixed(2)}%`);
    
    return { totalBytes, items };
  },
  
  // ============================================================
  // 7. 데이터 백업
  // ============================================================
  
  backup: function() {
    console.log('💾 데이터 백업 생성\n');
    
    const backup = {};
    
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      backup[key] = localStorage.getItem(key);
    }
    
    const blob = new Blob([JSON.stringify(backup, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = `stock-predictor-backup-${new Date().toISOString().slice(0,10)}.json`;
    a.click();
    
    URL.revokeObjectURL(url);
    
    console.log('✅ 백업 파일 다운로드됨');
    return backup;
  },
  
  // ============================================================
  // 8. 데이터 복구
  // ============================================================
  
  restore: function(backupJson) {
    console.log('🔄 데이터 복구\n');
    
    if (typeof backupJson === 'string') {
      try {
        backupJson = JSON.parse(backupJson);
      } catch (e) {
        console.error('❌ JSON 파싱 실패:', e);
        return false;
      }
    }
    
    let count = 0;
    for (const [key, value] of Object.entries(backupJson)) {
      localStorage.setItem(key, value);
      count++;
    }
    
    console.log(`✅ ${count}개 항목 복구됨`);
    console.log('⚠️ 페이지를 새로고침하세요!');
    
    return true;
  },
  
  // ============================================================
  // 9. 도움말
  // ============================================================
  
  help: function() {
    console.log(`
📚 Storage Debug 도움말
========================

사용 가능한 명령어:

  StorageDebug.viewAll()        - 전체 스토리지 조회
  StorageDebug.viewPortfolio()  - 포트폴리오 상세 조회
  StorageDebug.viewFavorites()  - 즐겨찾기 조회
  StorageDebug.viewAlerts()     - 알림 조회
  StorageDebug.viewBacktest()   - 백테스트 히스토리 조회
  StorageDebug.getUsage()       - 스토리지 사용량
  StorageDebug.backup()         - 데이터 백업 (JSON 다운로드)
  StorageDebug.restore(json)    - 데이터 복구
  StorageDebug.help()           - 이 도움말

또는 내장된 디버그 도구:
  window.__storageDebug.viewAll()
  window.__storageDebug.usage()

`);
  }
};

// 전역에 등록
window.StorageDebug = StorageDebug;

console.log('✅ StorageDebug 로드됨. StorageDebug.help()로 도움말 보기');

