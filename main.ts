import * as THREE from 'three';

const container = document.getElementById( 'container' );
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );

scene.background = new THREE.Color( 'rgb(230, 227, 226)' );

camera.position.z = 5;
scene.add( camera );

const helper = new THREE.GridHelper( 2000, 100 );
helper.position.y = -199;
helper.material.opacity = 0.50;
helper.material.transparent = true;
scene.add( helper );

// scene.add( new THREE.AmbientLight( 0xf0f0f0, 3 ) );

// const light = new THREE.SpotLight( 0xffffff, 4.5 );
// light.position.set( 0, 1500, 200 );
// light.angle = Math.PI * 0.2;
// light.decay = 0;
// light.castShadow = true;
// light.shadow.camera.near = 200;
// light.shadow.camera.far = 2000;
// light.shadow.bias = - 0.000222;
// light.shadow.mapSize.width = 1024;
// light.shadow.mapSize.height = 1024;
// scene.add( light );

const renderer = new THREE.WebGLRenderer();
renderer.setPixelRatio( window.devicePixelRatio );
renderer.setSize( window.innerWidth, window.innerHeight );
renderer.shadowMap.enabled = true;
container.appendChild( renderer.domElement );

renderer.render( scene, camera );