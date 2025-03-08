import * as THREE from 'three';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({
  canvas: document.getElementById('container'),
  antialias: true
});

// Generate and color the mesh
function generateMesh() {
  const size = 100;
  const scale = 10;
  const geometry = new THREE.PlaneGeometry(size, size, size, size);

  for (let i = 0; i < geometry.attributes.position.count; i++) {
    const x = (i % (size + 1)) / size * scale - scale / 2;
    const z = Math.floor(i / (size + 1)) / size * scale - scale / 2;
    const y = Math.sin(x) + Math.cos(z);
    geometry.attributes.position.setXYZ(i, x, y, z);
  }

  geometry.attributes.position.needsUpdate = true;

  return geometry;
}


function colorMesh(geometry) {
  const colors = [];
  for (let i = 0; i < geometry.attributes.position.count; i++) {
    const height = geometry.attributes.position.getY(i);
    const color = new THREE.Color();
    if (height < 0) {
      color.setHSL(0.33, 1, 0.5); // Blue for negative heights
    } else if (height > 0) {
      color.setHSL(0, 1, 0.5); // Red for positive heights
    } else {
      color.setHSL(0.5, 1, 0.5); // Green for zero height
    }
    colors.push(color.r, color.g, color.b);
  }
  geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
}


const geometry = generateMesh();
colorMesh(geometry);

const material = new THREE.MeshBasicMaterial({ vertexColors: true });
const mesh = new THREE.Mesh(geometry, material);

scene.add(mesh);

camera.position.z = 50;

function animate() {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}

animate();