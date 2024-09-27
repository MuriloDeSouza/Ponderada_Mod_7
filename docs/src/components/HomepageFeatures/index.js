import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const FeatureList = [
  {
    center: true,
    title: 'Pega esse vídeo top do funcionamento da Ponderada Mod 7',
    description: (
      <>
        Assista ao vídeo sobre o funcionamento da Ponderada Mod 7 clicando no link abaixo:
        <div style={{ marginTop: '20px' }}>
          <a 
            href="https://www.youtube.com/watch?v=8A30nVk0a4M" 
            target="_blank" 
            rel="noopener noreferrer"
            style={{ color: '#007bff', textDecoration: 'underline' }}
          >
            Assista ao vídeo no YouTube
          </a>
        </div>
      </>
    ),
  },
];

function Feature({ title, description }) {
  return (
    <div className={clsx('col col--12')}>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features} style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      minHeight: '100vh',
      textAlign: 'center'
    }}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
